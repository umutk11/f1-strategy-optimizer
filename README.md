# F1 Pit Strategy Optimizer

A ML-informed race strategy simulator for Formula 1.

This project explores how tyre degradation, pit-stop loss, traffic, and Safety Car scenarios affect race strategy decisions. Its goal is to simulate a full F1 grid and recommend the most effective one-stop, two-stop, or three-stop strategy for a target driver.

> **Project status:** Work in progress — V1 development has started.

## Problem Statement

Pit-stop strategy is not only about choosing the fastest tyre compound. A good decision also depends on:

- Tyre degradation over a stint
- Pit-lane time loss
- Traffic after rejoining the circuit
- Gaps to the leader and the car ahead
- DRS and overtaking opportunities
- Safety Car scenarios
- Strategies used by the other cars on the grid

This project models these factors to compare possible race strategies and identify the best expected outcome.

## First Case Study: 2024 Italian Grand Prix

The first backtesting case for this project is the **2024 Italian Grand Prix at Monza**.

| Item | Value |
|---|---|
| Circuit | Monza |
| Race length | 53 laps |
| Target driver | Charles Leclerc |
| Main question | Can the simulator identify why a one-stop strategy was competitive against two-stop alternatives? |

This race is a useful first case because it provides a meaningful comparison between Ferrari's successful one-stop approach and McLaren's more conservative two-stop strategy.

## V1 Scope

The first version focuses on dry-weather race simulations.

Planned capabilities:

- Simulate a 20-car F1 grid
- Model driver and team pace
- Model Soft, Medium, and Hard tyre compounds
- Estimate tyre degradation during each stint
- Simulate pit-stop loss and pit-lane rejoin position
- Track live race order, gap to leader, and interval to the car ahead
- Apply simplified traffic, DRS, and overtaking logic
- Generate Safety Car scenarios
- Compare one-stop, two-stop, and three-stop strategies automatically
- Run Monte Carlo simulations to account for uncertainty
- Display results in a Streamlit dashboard

## Out of Scope for V1

The following features are intentionally excluded from the first version:

- Wet and intermediate tyres
- Red flags and Virtual Safety Car
- Mechanical failures and DNFs
- Team orders
- Driver mistakes
- Real-time live race strategy recommendations
- Corner-by-corner physics simulation

## Simulation Design

For each race scenario, every car has its own state:

```text
driver
team
position
lap
sector
total race time
distance completed
tyre compound
tyre age
pit-stop count
planned strategy
race status
```

The simulator updates the grid over time and calculates:

```text
predicted lap time
+ tyre degradation
+ traffic penalty
+ pit-stop loss
+ Safety Car effects
= estimated race outcome
```

The target driver's strategies are scored using expected race time and risk:

```text
strategy_score = expected_race_time + risk_weight × result_variance
```

The strategy with the lowest score is recommended.

## Data

The project uses historical Formula 1 timing data, including:

- Lap and sector times
- Tyre compounds and tyre life
- Stint information
- Pit-stop events
- Grid and finishing positions
- Track status and Safety Car periods
- Weather data when available

The primary data source will be [FastF1](https://github.com/theOehrly/Fast-F1), a Python package for accessing Formula 1 timing, telemetry, and session data.

## Tech Stack

- Python 3.11+
- FastF1
- Pandas and NumPy
- Scikit-learn
- Matplotlib and Plotly
- Streamlit
- Pytest

## Limitations

This is a portfolio and learning project, not a professional F1 strategy system. Real-world race strategy depends on many unpredictable factors, including accidents, reliability issues, team orders, driver decisions, changing weather, and tyre condition details that may not be publicly available.

The goal is to build a transparent and explainable decision-support simulator rather than reproduce real race results perfectly.

## Future Improvements

- Dynamic strategy updates during a live race
- Rain and wet-tyre modelling
- Virtual Safety Car and red-flag scenarios
- Circuit-specific overtaking and pit-loss models
- More advanced tyre-degradation models
- Historical backtesting across multiple seasons
- Interactive strategy comparison dashboard

## Author

[Umut Kahraman](https://github.com/umutk11)
>>>>>>> 8edfb7e6732e53a9473f8e334d1fbe3ecb533879
