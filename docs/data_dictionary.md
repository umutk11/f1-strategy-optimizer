# Data Dictionary
This file describes the raw datasets that used in this project.
The initial dataset in this project is based on 2024 Italian Grand Prix at Autodromo Nazionale Monza 

## `monza_2024_race_laps.csv`

| Column | Description |
|---|---|
| Driver | Three-letter driver name abbreviation. |
| LapNumber | Completed lap count by the driver. |
| LapTime | Total time required to complete the lap. |
| Sector1Time | Time recorded in the first sector of the lap. |
| Sector2Time | Time recorded in the second sector of the lap. |
| Sector3Time | Time recorded in the third sector of the lap. |
| Position | Driver's race position at the end of the lap. |
| Stint | Tyre stint number. A new stint begins after a pit stop. |
| Compound | Tyre compound used on the lap.(Soft/Medium/Hard) |
| TyreLife | Number of laps completed on the current tyre set. |
| PitInTime | Session time at which the driver entered the pit lane. |
| PitOutTime | Session time at which the driver left the pit lane. |
| TrackStatus | Track condition code for the lap. |
| IsAccurate | Indicates whether FastF1 considers the lap timing data reliable. |

## `monza_2024_race_results.csv`

| Column | Description |
|---|---|
| Abbreviation | Three-letter driver abbreviation. |
| TeamName | Constructor/team name. |
| GridPosition | Starting grid position. |
| Position | Final classified race position. |
| Status | Final race status, such as Finished, Lapped, or Retired. |

## `monza_2024_weather.csv`

| Column | Description |
|---|---|
| Time | Session-relative timestamp of the weather observation. |
| AirTemp | Ambient air temperature in degrees Celsius. |
| TrackTemp | Track surface temperature in degrees Celsius. |
| Humidity | Relative humidity as a percentage. |
| Pressure | Atmospheric pressure in millibars. |
| Rainfall | Indicates whether rainfall was recorded. |
| WindDirection | Wind direction in degrees. |
| WindSpeed | Wind speed in metres per second. |

## `monza_2024_event_metadata.json`

Contains race-level metadata, including the season, round number, event name, circuit location, country, and session dates.