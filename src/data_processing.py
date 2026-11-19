from pathlib import Path

import pandas as pd


# find the project folder from this file
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


def load_raw_data(raw_dir):
    laps = pd.read_csv(raw_dir / "monza_2024_race_laps.csv")
    results = pd.read_csv(raw_dir / "monza_2024_race_results.csv")
    return laps, results


def prepare_laps(laps, results):
    # keep the raw lap data unchanged
    laps = laps.copy()

    # standardize driver abbreviations
    laps["Driver"] = laps["Driver"].astype("string").str.strip().str.upper()

    # change lap times from text to seconds
    laps["LapTimeSeconds"] = (
        pd.to_timedelta(laps["LapTime"], errors="coerce")
        .dt.total_seconds()
    )

    # change each sector time to seconds
    for column in ["Sector1Time", "Sector2Time", "Sector3Time"]:
        new_column = column.replace("Time", "Seconds")
        laps[new_column] = (
            pd.to_timedelta(laps[column], errors="coerce")
            .dt.total_seconds()
        )

    # mark laps when a driver enters or leaves the pit lane
    laps["IsPitInLap"] = laps["PitInTime"].notna()
    laps["IsPitOutLap"] = laps["PitOutTime"].notna()
    laps["IsPitRelatedLap"] = laps["IsPitInLap"] | laps["IsPitOutLap"]
    # track status 4 indicates Safety Car
    laps["IsSafetyCarLap"] = (
        laps["TrackStatus"]
        .astype("string")
        .str.contains("4", regex=False, na=False)
    )

    # select and standardize driver details
    driver_info = results[
        ["Abbreviation", "TeamName", "GridPosition", "Status"]
    ].copy()

    driver_info["Abbreviation"] = (
        driver_info["Abbreviation"]
        .astype("string")
        .str.strip()
        .str.upper()
    )
    driver_info = driver_info.rename(columns={"Abbreviation": "Driver"})

    # add driver details to all laps
    laps = laps.merge(
        driver_info,
        on="Driver",
        how="left",
        validate="many_to_one",
    )

    # sort laps by driver and lap number
    laps = laps.sort_values(["Driver", "LapNumber"]).copy()

    # add lap times for each driver
    laps["ElapsedLapTimeSeconds"] = (
        laps.groupby("Driver")["LapTimeSeconds"].cumsum().round(3)
    )

    return laps


def validate_laps(laps):
    # stop if one driver has the same lap number twice
    if laps.duplicated(["Driver", "LapNumber"]).any():
        raise ValueError("A driver has a repeated lap number.")

    # stop if a lap time is missing or zero
    if laps["LapTimeSeconds"].isna().any():
        raise ValueError("Some lap times could not be converted.")

    # stop if a lap time is zero or negative
    if (laps["LapTimeSeconds"] <= 0).any():
        raise ValueError("A lap time is zero or negative.")

    # stop if a driver is missing or not found in race results
    if laps["Driver"].isna().any() or laps["TeamName"].isna().any():
        raise ValueError("A driver is missing or not found in race results.")

    # stop if stint or tyre life is missing or invalid
    if laps[["Stint", "TyreLife"]].isna().any().any():
        raise ValueError("Stint or tyre life is missing.")

    # stop if stint or tyre life is invalid
    if (laps["Stint"] < 1).any() or (laps["TyreLife"] < 0).any():
        raise ValueError("Stint or tyre life has an invalid value.")


def format_duration(value, include_hours=False):
    if pd.isna(value):
        return ""

    milliseconds = round(pd.to_timedelta(value).total_seconds() * 1000)
    total_seconds, milliseconds = divmod(milliseconds, 1000)
    total_minutes, seconds = divmod(total_seconds, 60)

    if include_hours:
        hours, minutes = divmod(total_minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    return f"{total_minutes:02d}:{seconds:02d}:{milliseconds:03d}"


def format_time_columns(laps):
    laps = laps.copy()

    # show lap and sector durations as mm:ss:msms
    for column in ["LapTime", "Sector1Time", "Sector2Time", "Sector3Time"]:
        laps[column] = laps[column].map(format_duration)

    # show session timestamps without the days prefix
    session_columns = [
        "Time",
        "PitOutTime",
        "PitInTime",
        "Sector1SessionTime",
        "Sector2SessionTime",
        "Sector3SessionTime",
        "LapStartTime",
    ]

    for column in session_columns:
        laps[column] = laps[column].map(
            lambda value: format_duration(value, include_hours=True)
        )

    return laps


def main():
    # prepare and check the data before saving it
    laps, results = load_raw_data(RAW_DIR)
    processed_laps = prepare_laps(laps, results)
    validate_laps(processed_laps)
    processed_laps = format_time_columns(processed_laps)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_laps.to_csv(
        PROCESSED_DIR / "monza_2024_laps.csv",
        index=False,
    )


if __name__ == "__main__":
    main()