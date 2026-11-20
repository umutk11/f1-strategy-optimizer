import pandas as pd
import pytest

from src.pace_model import (
    fit_pace_model,
    fuel_penalty,
    mean_absolute_error,
    predict_lap_time,
    predict_lap_times,
    select_clean_laps,
)


CIRCUIT = {"fuel_s_per_kg": 0.03, "start_fuel_kg": 110, "total_laps": 50}
BASE_PACE = {"AAA": 80.0, "BBB": 80.5, "CCC": 81.0}
OFFSET = {"HARD": 0.0, "MEDIUM": -0.4}
RATE = {"HARD": 0.03, "MEDIUM": 0.06}


def synthetic_laps():
    rows = []
    for driver, base in BASE_PACE.items():
        for lap in range(2, 51):
            compound = "MEDIUM" if lap <= 20 else "HARD"
            tyre_life = lap if lap <= 20 else lap - 20
            lap_time = (
                base
                + OFFSET[compound]
                + RATE[compound] * tyre_life
                + fuel_penalty(lap, **CIRCUIT)
            )
            rows.append({
                "Driver": driver,
                "LapNumber": lap,
                "Compound": compound,
                "TyreLife": tyre_life,
                "LapTimeSeconds": lap_time,
                "IsPitRelatedLap": False,
                "IsSafetyCarLap": False,
                "IsAccurate": True,
                "IncludeInSimulation": True,
            })
    return pd.DataFrame(rows)


def test_fit_recovers_known_parameters():
    model = fit_pace_model(synthetic_laps(), CIRCUIT)

    for driver, pace in BASE_PACE.items():
        assert model.driver_base_pace[driver] == pytest.approx(pace)
    assert model.compound_offset["MEDIUM"] == pytest.approx(OFFSET["MEDIUM"])
    assert model.degradation_rate["HARD"] == pytest.approx(RATE["HARD"])
    assert model.degradation_rate["MEDIUM"] == pytest.approx(RATE["MEDIUM"])


def test_prediction_error_is_zero_on_exact_data():
    laps = synthetic_laps()
    model = fit_pace_model(laps, CIRCUIT)

    assert mean_absolute_error(predict_lap_times(model, laps)) == pytest.approx(0)


def test_select_clean_laps_removes_unusable_laps():
    laps = synthetic_laps()
    laps.loc[0, "LapNumber"] = 1
    laps.loc[1, "IsPitRelatedLap"] = True
    laps.loc[2, "IsSafetyCarLap"] = True
    laps.loc[3, "IsAccurate"] = False
    laps.loc[4, "IncludeInSimulation"] = False
    laps.loc[5, "LapTimeSeconds"] = 120.0

    clean = select_clean_laps(laps)

    assert not clean.index.isin(range(6)).any()
    assert len(clean) == len(laps) - 6


def test_select_clean_laps_drops_rare_compound():
    laps = synthetic_laps()
    laps.loc[10, "Compound"] = "SOFT"

    assert "SOFT" not in select_clean_laps(laps)["Compound"].values


def test_unknown_compound_raises():
    model = fit_pace_model(synthetic_laps(), CIRCUIT)

    with pytest.raises(ValueError):
        predict_lap_time(model, "AAA", "SOFT", 5, 10)


def test_fuel_penalty_falls_during_race():
    first = fuel_penalty(1, **CIRCUIT)
    last = fuel_penalty(50, **CIRCUIT)

    assert first == pytest.approx(0.03 * 110)
    assert last < first
