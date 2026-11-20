# Data Dictionary
This file describes the raw datasets that used in this project.
The initial dataset in this project is based on 2024 Italian Grand Prix at Autodromo Nazionale Monza 

## `monza_2024_race_laps.csv`

| Column | Description |
|---|---|
| Driver | Three-letter driver name abbreviation. |
| LapNumber | Completed lap count by the driver. |
| LapTime | Total time required to complete the lap. |
| Sector1Time | Time recorded in the first sector of the lap. Empty on lap 1 because the race starts from the grid. |
| Sector2Time | Time recorded in the second sector of the lap. |
| Sector3Time | Time recorded in the third sector of the lap. |
| Position | Driver's race position at the end of the lap. |
| Stint | Tyre stint number. A new stint begins after a pit stop. |
| Compound | Tyre compound used on the lap.(Soft/Medium/Hard) |
| TyreLife | Number of laps completed on the current tyre set, including use before the race. |
| PitInTime | Session time at which the driver entered the pit lane. |
| PitOutTime | Session time at which the driver left the pit lane. |
| TrackStatus | Track condition code for the lap. |
| IsAccurate | Indicates whether FastF1 considers the lap timing data reliable. |
| Time | Session time at which the lap was completed. |
| DriverNumber | Driver's car number. |
| Sector1SessionTime | Session time at which the first sector was completed. |
| Sector2SessionTime | Session time at which the second sector was completed. |
| Sector3SessionTime | Session time at which the third sector was completed. |
| SpeedI1 | Speed trap value at the first intermediate point (km/h). |
| SpeedI2 | Speed trap value at the second intermediate point (km/h). |
| SpeedFL | Speed at the finish line (km/h). |
| SpeedST | Speed at the longest straight speed trap (km/h). |
| IsPersonalBest | Indicates whether the lap is the driver's personal best at that moment. |
| FreshTyre | Indicates whether the tyre set was new when fitted. |
| Team | Team name as reported in the lap data. |
| LapStartTime | Session time at which the lap started. |
| LapStartDate | Wall-clock date and time at which the lap started. |
| Deleted | Indicates whether the lap time was deleted by the stewards. |
| DeletedReason | Reason for a deleted lap time. |
| FastF1Generated | Indicates whether FastF1 generated the lap because timing data was incomplete. |

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

## `config/circuits.json`

Circuit-level constants used by the simulation.

| Field | Description |
|---|---|
| circuit_name | Official circuit name. |
| season | Season of the race. |
| event_name | Grand Prix name. |
| circuit_length_km | Length of one lap in kilometres. |
| total_laps | Scheduled race laps. |
| race_distance_km | Total race distance in kilometres. |
| start_fuel_kg | Fuel on board at the race start (2024 maximum: 110 kg). |
| fuel_s_per_kg | Lap time cost of each kilogram of fuel on board, in seconds. |

## `data/processed/monza_2024_laps.csv`

Created by `src/data_processing.py`. It keeps all raw lap columns and adds the columns below. Lap, sector and session times are written as text (`mm:ss:mmm` and `hh:mm:ss.mmm`); use the `...Seconds` columns for calculations.

| Column | Description |
|---|---|
| LapTimeSeconds | Lap time in seconds. |
| Sector1Seconds | First sector time in seconds. Empty on lap 1. |
| Sector2Seconds | Second sector time in seconds. |
| Sector3Seconds | Third sector time in seconds. |
| IsPitInLap | True if the driver entered the pit lane on this lap. |
| IsPitOutLap | True if the driver left the pit lane on this lap. |
| IsPitRelatedLap | True if the lap is a pit-in or pit-out lap. |
| IsSafetyCarLap | True if the Safety Car was out during the lap (track status 4). |
| TeamName | Team name from the race results. |
| GridPosition | Starting grid position. |
| Status | Final race status. |
| IncludeInSimulation | False for drivers who retired from the race. |
| StintNumber | Stint number derived from pit-out laps. |
| TyreAge | Laps driven on the current tyre set in this race. Resets to 1 after a pit stop. |
| ElapsedLapTimeSeconds | Cumulative race time of the driver at the end of the lap. |
