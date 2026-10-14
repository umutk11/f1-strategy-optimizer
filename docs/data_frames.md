# Data Frames
This file explains data frames that created in 01_eda.ipynb notebook.

## `results_summary`

A summary of the final race classification.

| Column | Description |
|---|---|
| Abbreviation | Three-letter driver abbreviation. |
| TeamName | Constructor/team name. |
| GridPosition | Starting grid position. |
| Position | Final classified race position. |
| Status | Final race status. |

## `starting_grid`

Drivers ordered by their grid position at the start(after qualifying sessions).

| Column | Description |
|---|---|
| Abbreviation | Three-letter driver abbreviation. |
| TeamName | Constructor/team name. |
| GridPosition | Starting grid position. |
| Position | Final classified race position. |
| Status | Final race status. |

## `race_laps`

Lap and sector data for all drivers.

| Column | Description |
|---|---|
| Driver | Three-letter driver abbreviation. |
| LapNumber | Lap number completed by the driver. |
| LapTime | Total lap duration. |
| Sector1Time | First sector duration. |
| Sector2Time | Second sector duration. |
| Sector3Time | Third sector duration. |
| Position | Driver position at the end of the lap. |
| IsAccurate | FastF1 timing-quality indicator. |

## `race_strategy_laps`

Lap-level strategy data.

| Column | Description |
|---|---|
| Driver | Three-letter driver abbreviation. |
| LapNumber | Lap number completed by the driver. |
| Position | Driver position at the end of the lap. |
| Stint | Tyre stint number. |
| Compound | Tyre compound used. |
| TyreLife | Laps completed on the current tyre set. |
| LapTime | Total lap duration. |
| PitInTime | Session time at pit-lane entry. |
| PitOutTime | Session time at pit-lane exit. |
| TrackStatus | Track condition code. |
| IsAccurate | FastF1 timing-quality indicator. |
| IsPitInLap | Indicates a pit-entry lap. |
| IsPitOutLap | Indicates a pit-exit lap. |
| IsPitRelatedLap | Indicates either a pit-entry or pit-exit lap. |
| HasSafetyCar | Indicates whether the lap occurred under Safety Car conditions. |
| HasVSC | Indicates whether the lap occurred under Virtual Safety Car conditions. |
| HasYellowFlag | Indicates whether the lap contains a yellow-flag track status. |

## `pit_laps`

Subset of `race_strategy_laps` containing pit-related laps only.

| Column | Description |
|---|---|
| Driver | Three-letter driver abbreviation. |
| LapNumber | Pit-related lap number. |
| PitInTime | Session time at pit-lane entry, if applicable. |
| PitOutTime | Session time at pit-lane exit, if applicable. |
| Compound | Tyre compound used. |
| Stint | Tyre stint number. |
| IsPitInLap | Indicates a pit-entry lap. |
| IsPitOutLap | Indicates a pit-exit lap. |

## `leclerc_laps`

Selected lap-level data for Charles Leclerc.

| Column | Description |
|---|---|
| Stint | Tyre stint number. |
| LapNumber | Lap number completed. |
| LapTime | Total lap duration. |
| Position | Race position at the end of the lap. |
| Compound | Tyre compound used. |
| TyreLife | Laps completed on the current tyre set. |
| PitInTime | Session time at pit-lane entry. |
| PitOutTime | Session time at pit-lane exit. |
| TrackStatus | Track condition code. |
| IsAccurate | FastF1 timing-quality indicator. |

## `weather_data`

Time-based weather observations during the race.

| Column | Description |
|---|---|
| Time | Session-relative weather observation time. |
| AirTemp | Ambient air temperature in degrees Celsius. |
| Humidity | Relative humidity percentage. |
| Pressure | Atmospheric pressure in millibars. |
| Rainfall | Indicates whether rainfall was recorded. |
| TrackTemp | Track surface temperature in degrees Celsius. |
| WindDirection | Wind direction in degrees. |
| WindSpeed | Wind speed in metres per second. |

## `race_classification`

Race classification used to determine simulation eligibility.

| Column | Description |
|---|---|
| Abbreviation | Three-letter driver abbreviation. |
| TeamName | Constructor/team name. |
| GridPosition | Starting grid position. |
| Position | Final classified race position. |
| Status | Original final race status. |
| RaceClassification | Simplified classification, including DNF. |
| IncludeInBaselineSimulation | Indicates whether the driver is included in the baseline simulation. |