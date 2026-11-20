import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROCESSED_LAPS_PATH = PROJECT_ROOT / "data" / "processed" / "monza_2024_laps.csv"
CIRCUITS_PATH = PROJECT_ROOT / "config" / "circuits.json"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

REFERENCE_COMPOUND = "HARD"
MIN_COMPOUND_LAPS = 20
MIN_COMPOUND_DRIVERS = 3
SLOW_LAP_RATIO = 1.07


@dataclass
class PaceModel:
    driver_base_pace: dict
    compound_offset: dict
    degradation_rate: dict
    fuel_s_per_kg: float
    start_fuel_kg: float
    total_laps: int


def load_circuit(name, path=CIRCUITS_PATH):
    with open(path, encoding="utf-8") as file:
        return json.load(file)[name]


def select_clean_laps(laps):
    # keep only green-flag racing laps with reliable timing
    clean = laps[
        ~laps["IsPitRelatedLap"]
        & ~laps["IsSafetyCarLap"]
        & (laps["LapNumber"] > 1)
        & laps["IsAccurate"]
        & laps["IncludeInSimulation"]
        & laps["LapTimeSeconds"].notna()
    ].copy()

    # drop compounds with too little data for a reliable estimate
    compound_stats = clean.groupby("Compound").agg(
        laps=("LapTimeSeconds", "size"),
        drivers=("Driver", "nunique"),
    )
    reliable = compound_stats[
        (compound_stats["laps"] >= MIN_COMPOUND_LAPS)
        & (compound_stats["drivers"] >= MIN_COMPOUND_DRIVERS)
    ].index
    clean = clean[clean["Compound"].isin(reliable)]

    # drop laps far slower than the driver's usual pace (traffic, mistakes)
    driver_median = clean.groupby("Driver")["LapTimeSeconds"].transform("median")
    return clean[clean["LapTimeSeconds"] <= driver_median * SLOW_LAP_RATIO].copy()


def fuel_penalty(lap_number, fuel_s_per_kg, start_fuel_kg, total_laps):
    # fuel burns linearly, so the car is heaviest on lap 1
    fuel_kg = start_fuel_kg * (total_laps - lap_number + 1) / total_laps
    return fuel_s_per_kg * fuel_kg


def fit_pace_model(clean_laps, circuit):
    drivers = sorted(clean_laps["Driver"].unique())
    compounds = sorted(clean_laps["Compound"].unique())
    offset_compounds = [c for c in compounds if c != REFERENCE_COMPOUND]

    # remove the fuel effect first, then fit everything else at once
    target = clean_laps["LapTimeSeconds"] - fuel_penalty(
        clean_laps["LapNumber"],
        circuit["fuel_s_per_kg"],
        circuit["start_fuel_kg"],
        circuit["total_laps"],
    )

    columns = [(clean_laps["Driver"] == d).astype(float) for d in drivers]
    columns += [(clean_laps["Compound"] == c).astype(float) for c in offset_compounds]
    columns += [
        (clean_laps["Compound"] == c) * clean_laps["TyreLife"] for c in compounds
    ]
    design = np.column_stack(columns)
    coefficients, *_ = np.linalg.lstsq(design, target.to_numpy(), rcond=None)
    coefficients = coefficients.tolist()

    driver_values = coefficients[: len(drivers)]
    offset_values = coefficients[len(drivers): len(drivers) + len(offset_compounds)]
    rate_values = coefficients[len(drivers) + len(offset_compounds):]

    compound_offset = {c: 0.0 for c in compounds}
    compound_offset.update(dict(zip(offset_compounds, offset_values)))

    return PaceModel(
        driver_base_pace=dict(zip(drivers, driver_values)),
        compound_offset=compound_offset,
        degradation_rate=dict(zip(compounds, rate_values)),
        fuel_s_per_kg=circuit["fuel_s_per_kg"],
        start_fuel_kg=circuit["start_fuel_kg"],
        total_laps=circuit["total_laps"],
    )


def predict_lap_time(model, driver, compound, tyre_life, lap_number):
    if driver not in model.driver_base_pace:
        raise ValueError(f"No pace data for driver {driver}.")
    if compound not in model.compound_offset:
        raise ValueError(f"No pace data for compound {compound}.")

    return (
        model.driver_base_pace[driver]
        + model.compound_offset[compound]
        + model.degradation_rate[compound] * tyre_life
        + fuel_penalty(
            lap_number,
            model.fuel_s_per_kg,
            model.start_fuel_kg,
            model.total_laps,
        )
    )


def predict_lap_times(model, laps):
    laps = laps.copy()
    laps["PredictedLapTimeSeconds"] = [
        predict_lap_time(model, driver, compound, tyre_life, lap_number)
        for driver, compound, tyre_life, lap_number in zip(
            laps["Driver"], laps["Compound"], laps["TyreLife"], laps["LapNumber"]
        )
    ]
    laps["PredictionError"] = (
        laps["PredictedLapTimeSeconds"] - laps["LapTimeSeconds"]
    )
    return laps


def mean_absolute_error(predicted_laps):
    return predicted_laps["PredictionError"].abs().mean()


def worst_predictions(predicted_laps, n=10):
    order = predicted_laps["PredictionError"].abs().sort_values(ascending=False)
    return predicted_laps.loc[order.index[:n]]


def estimate_fuel_effect_from_data(clean_laps):
    # free fit of a per-lap trend, only used to compare with the config value
    drivers = sorted(clean_laps["Driver"].unique())
    compounds = sorted(clean_laps["Compound"].unique())
    columns = [(clean_laps["Driver"] == d).astype(float) for d in drivers]
    columns += [
        (clean_laps["Compound"] == c).astype(float)
        for c in compounds
        if c != REFERENCE_COMPOUND
    ]
    columns += [
        (clean_laps["Compound"] == c) * clean_laps["TyreLife"] for c in compounds
    ]
    columns.append(clean_laps["LapNumber"].astype(float))
    design = np.column_stack(columns)
    coefficients, *_ = np.linalg.lstsq(
        design, clean_laps["LapTimeSeconds"].to_numpy(), rcond=None
    )
    return -coefficients[-1]


def main():
    circuit = load_circuit("monza")
    laps = pd.read_csv(PROCESSED_LAPS_PATH)
    clean_laps = select_clean_laps(laps)
    model = fit_pace_model(clean_laps, circuit)
    predicted = predict_lap_times(model, clean_laps)

    config_fuel_per_lap = (
        circuit["fuel_s_per_kg"] * circuit["start_fuel_kg"] / circuit["total_laps"]
    )

    print(f"Clean laps used: {len(clean_laps)} of {len(laps)}")
    print("\nDriver base pace (s):")
    for driver, pace in sorted(model.driver_base_pace.items(), key=lambda x: x[1]):
        print(f"  {driver}: {pace:.3f}")
    print("\nCompound offset (s):", {k: round(v, 3) for k, v in model.compound_offset.items()})
    print("Degradation rate (s/lap):", {k: round(v, 4) for k, v in model.degradation_rate.items()})
    print(f"\nFuel effect from config: {config_fuel_per_lap:.4f} s/lap")
    print(f"Fuel effect from data:   {estimate_fuel_effect_from_data(clean_laps):.4f} s/lap")
    print(f"\nMAE: {mean_absolute_error(predicted):.3f} s")
    print("\nWorst 10 predictions:")
    print(
        worst_predictions(predicted)[
            [
                "Driver",
                "LapNumber",
                "Compound",
                "TyreLife",
                "LapTimeSeconds",
                "PredictedLapTimeSeconds",
                "PredictionError",
            ]
        ].round(3).to_string(index=False)
    )

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    predicted.to_csv(OUTPUTS_DIR / "pace_predictions.csv", index=False)


if __name__ == "__main__":
    main()
