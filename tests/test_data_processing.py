import pandas as pd

from src.data_processing import prepare_laps, validate_laps


def sample_data():
    laps = pd.DataFrame({
        "Driver": [" alb ", "ALB"],
        "LapNumber": [1, 2],
        "LapTime": ["0 days 00:01:30", "0 days 00:01:29"],
        "Sector1Time": ["0 days 00:00:30", "0 days 00:00:29"],
        "Sector2Time": ["0 days 00:00:30", "0 days 00:00:30"],
        "Sector3Time": ["0 days 00:00:30", "0 days 00:00:30"],
        "PitInTime": [pd.NA, "0 days 01:00:00"],
        "PitOutTime": [pd.NA, pd.NA],
        "TrackStatus": ["1", "4"],
        "Stint": [1, 1],
        "TyreLife": [1, 2],
    })

    results = pd.DataFrame({
        "Abbreviation": ["ALB"],
        "TeamName": ["Williams"],
        "GridPosition": [9],
        "Status": ["Finished"],
    })
    return laps, results


def test_lap_and_sector_times_are_converted():
    laps, results = sample_data()
    processed = prepare_laps(laps, results)

    assert processed["LapTimeSeconds"].tolist() == [90.0, 89.0]
    assert processed["Sector1Seconds"].tolist() == [30.0, 29.0]


def test_pit_flags():
    laps, results = sample_data()
    processed = prepare_laps(laps, results)

    assert processed["IsPitInLap"].tolist() == [False, True]
    assert processed["IsPitRelatedLap"].tolist() == [False, True]


def test_safety_car_flag():
    laps, results = sample_data()
    processed = prepare_laps(laps, results)

    assert processed["IsSafetyCarLap"].tolist() == [False, True]


def test_driver_and_cumulative_time():
    laps, results = sample_data()
    processed = prepare_laps(laps, results)
    validate_laps(processed)

    assert processed["Driver"].tolist() == ["ALB", "ALB"]
    assert processed["ElapsedLapTimeSeconds"].tolist() == [90.0, 179.0]


def test_stint_and_tyre_age_reset_after_pit_stop():
    laps = pd.DataFrame({
        "Driver": ["ALB"] * 4,
        "LapNumber": [1, 2, 3, 4],
        "LapTime": ["0 days 00:01:30"] * 4,
        "Sector1Time": ["0 days 00:00:30"] * 4,
        "Sector2Time": ["0 days 00:00:30"] * 4,
        "Sector3Time": ["0 days 00:00:30"] * 4,
        "PitInTime": [pd.NA, "0 days 01:00:00", pd.NA, pd.NA],
        "PitOutTime": [pd.NA, pd.NA, "0 days 01:00:20", pd.NA],
        "TrackStatus": ["1"] * 4,
        "Stint": [1, 1, 2, 2],
        "TyreLife": [1, 2, 3, 4],
    })
    _, results = sample_data()
    processed = prepare_laps(laps, results)
    validate_laps(processed)

    assert processed["StintNumber"].tolist() == [1, 1, 2, 2]
    assert processed["TyreAge"].tolist() == [1, 2, 1, 2]


def test_retired_driver_is_excluded_from_simulation():
    laps, results = sample_data()
    results["Status"] = "Retired"
    processed = prepare_laps(laps, results)

    assert processed["IncludeInSimulation"].tolist() == [False, False]


def test_finished_driver_is_included_in_simulation():
    laps, results = sample_data()
    processed = prepare_laps(laps, results)

    assert processed["IncludeInSimulation"].tolist() == [True, True]