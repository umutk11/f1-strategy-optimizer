from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

def load_raw_data(raw_dir):
    laps = pd.read_csv(raw_dir / "monza_2024_race_laps.csv")
    results = pd.read_csv(raw_dir / "monza_2024_race_results.csv")
    return laps, results

laps, results = load_raw_data(RAW_DIR)

laps["LapTimeSeconds"] = (
    pd.to_timedelta(laps["LapTime"], errors="coerce")
    .dt.total_seconds()
)

for column in ["Sector1Time", "Sector2Time", "Sector3Time"]:
    new_column = column.replace("Time", "Seconds")
    laps[new_column] = (
        pd.to_timedelta(laps[column], errors="coerce")
        .dt.total_seconds()
    )

laps["IsPitInLap"] = laps["PitInTime"].notna()
laps["IsPitOutLap"] = laps["PitOutTime"].notna()

laps["IsPitRelatedLap"] = (
    laps["IsPitInLap"] | laps["IsPitOutLap"]
)

driver_info = results[
    ["Abbreviation", "TeamName", "GridPosition", "Status"]
].rename(columns={"Abbreviation": "Driver"})

laps = laps.merge(
    driver_info,
    on="Driver",
    how="left",
    validate="many_to_one",
)

laps = laps.sort_values(["Driver", "LapNumber"]).copy()

laps["ElapsedLapTimeSeconds"] = (
    laps.groupby("Driver")["LapTimeSeconds"].cumsum()
)

def prepare_laps(laps, results):
    laps = laps.copy()

    laps["LapTimeSeconds"] = (
        pd.to_timedelta(laps["LapTime"], errors="coerce")
        .dt.total_seconds()
    )

    laps["IsPitInLap"] = laps["PitInTime"].notna()
    laps["IsPitOutLap"] = laps["PitOutTime"].notna()

    return laps

def validate_laps(laps):
    if laps.duplicated(["Driver", "LapNumber"]).any():
        raise ValueError("Aynı sürücü ve tur numarası tekrar ediyor.")

    if laps["LapTimeSeconds"].isna().any():
        raise ValueError("Çevrilemeyen tur süresi var.")

    if (laps["LapTimeSeconds"] <= 0).any():
        raise ValueError("Sıfır veya negatif tur süresi var.")

def main():
    laps, results = load_raw_data(RAW_DIR)
    processed_laps = prepare_laps(laps, results)
    validate_laps(processed_laps)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    processed_laps.to_csv(
        PROCESSED_DIR / "monza_2024_laps.csv",
        index=False,
    )


if __name__ == "__main__":
    main()