# Where the charge saves time (NetLogo, seed 1)

Charged run vs its no-charge run (same seed and agents), the charged days 6-10. Section values from the NetLogo model every 5 minutes, 06:00-10:00. Vehicles are real vehicles (background traffic plus 20 cars per commuter agent). Vehicle-hours of delay: summed over the whole 06:00-10:00 morning, so delay moved into the shoulders by retiming is counted. 'Minutes per car' on a street: delay over the street's simulated sections for a car driving all of them, 07:00-09:00, weighted by traffic. Commuter minutes = road delay plus gate queue per car trip of the commuters who still drive (served trips). SA2 rows rest on 8-27 commuter agents each and are indicative only.

## R-daily_mock_py_s1 vs R-daily_mock_py_s1_peak0

- Commuter car trips per day: 800 without the charge, 634 with it.
- Delay per remaining car trip (road + gate queue): 7.1 -> 5.5 min (mean over drivers; door to door 18.6 -> 17.1 min).
- All vehicles on the simulated roads, 06:00-10:00: 28,975 vehicle-hours of delay per morning without the charge, 1,326 fewer with it (4.6%).

### Roads with the largest total saving (vehicle-hours of delay per morning, 06:00-10:00)

Per car: delay over the street's simulated sections, 07:00-09:00, weighted by traffic.

| street | motorway | km | delay per car, no charge (min) | with charge | minutes saved per car | % cut | vehicle-hours saved | % of street's delay |
|---|---|---|---|---|---|---|---|---|
| Southwestern Motorway | yes | 18.5 | 2.38 | 1.70 | 0.68 | 29% | 95 | 23% |
| Northern Motorway | yes | 25.4 | 19.87 | 19.87 | 0.00 | 0% | 90 | 2% |
| Northwestern Motorway | yes | 25.1 | 17.44 | 17.24 | 0.21 | 1% | 80 | 2% |
| Manukau Road |  | 4.1 | 4.13 | 2.79 | 1.34 | 33% | 55 | 35% |
| Mount Eden Road |  | 4.9 | 5.82 | 4.06 | 1.76 | 30% | 51 | 31% |
| Dominion Road |  | 6.1 | 5.53 | 4.51 | 1.02 | 18% | 51 | 21% |
| Tamaki Drive |  | 9.7 | 9.52 | 8.19 | 1.33 | 14% | 45 | 15% |
| Pakuranga Road |  | 6.2 | 4.05 | 3.71 | 0.33 | 8% | 31 | 8% |
| East Coast Road |  | 5.0 | 3.75 | 2.32 | 1.43 | 38% | 27 | 27% |
| Entry 424 Fanshawe Street |  | 0.6 | 0.57 | 0.24 | 0.33 | 58% | 26 | 58% |
| Great North Road |  | 12.4 | 8.79 | 8.18 | 0.61 | 7% | 25 | 6% |
| Entry 429 Wellesley Street |  | 0.7 | 0.80 | 0.47 | 0.33 | 42% | 24 | 46% |

### Roads where delay grew (vehicle-hours per morning)

| street | km | vehicle-hours added | minutes per car 07:00-09:00, no charge -> charge |
|---|---|---|---|
| Southern Motorway | 41.9 | 17 | 28.81 -> 28.91 |
| Murphys Road | 2.1 | 2 | 2.31 -> 2.38 |
| Glenvar Road | 1.9 | 2 | 2.15 -> 2.06 |
| Ashley Avenue | 0.2 | 0 | 0.15 -> 0.15 |
| Deep Creek Road | 1.7 | 0 | 1.17 -> 1.20 |

### Roads with the largest saving per car (at least 1 km simulated)

| street | km | delay per car, no charge (min) | with charge | minutes saved per car | % cut |
|---|---|---|---|---|---|
| Mount Eden Road | 4.9 | 5.82 | 4.06 | 1.76 | 30% |
| East Coast Road | 5.0 | 3.75 | 2.32 | 1.43 | 38% |
| Manukau Road | 4.1 | 4.13 | 2.79 | 1.34 | 33% |
| Tamaki Drive | 9.7 | 9.52 | 8.19 | 1.33 | 14% |
| Dominion Road | 6.1 | 5.53 | 4.51 | 1.02 | 18% |
| Chivalry Road | 1.6 | 2.39 | 1.58 | 0.81 | 34% |
| Southwestern Motorway | 18.5 | 2.38 | 1.70 | 0.68 | 29% |
| Great North Road | 12.4 | 8.79 | 8.18 | 0.61 | 7% |
| Ngapipi Road | 1.3 | 1.33 | 0.77 | 0.56 | 42% |
| Kepa Road | 2.4 | 1.76 | 1.32 | 0.44 | 25% |

### By road region

| region | km | vehicle-hours saved (06-10) | % of its delay | per km | mean V/C 07-09, no charge -> charge | LoS E/F by speed 07-09 |
|---|---|---|---|---|---|---|
| Other roads | 368 | 804 | 7.5% | 2.2 | 1.36 -> 1.34 | 7% -> 5% |
| North Shore | 64 | 131 | 6.9% | 2.1 | 1.39 -> 1.37 | 12% -> 11% |
| SH20 | 19 | 108 | 24.4% | 5.6 | 0.94 -> 0.93 | 8% -> 3% |
| Green Lane | 11 | 81 | 20.8% | 7.4 | 1.38 -> 1.33 | 5% -> 2% |
| SH16 | 25 | 80 | 2.0% | 3.2 | 0.84 -> 0.82 | 83% -> 81% |
| SH1 | 67 | 73 | 0.7% | 1.1 | 0.86 -> 0.83 | 96% -> 96% |
| New Lynn | 24 | 49 | 7.0% | 2.0 | 1.40 -> 1.38 | 9% -> 8% |

### By where commuters live (delay per remaining car trip, min)

| group | commuters | car trips/day no charge -> charge | delay no charge | with charge | minutes saved |
|---|---|---|---|---|---|
| E | 69 | 61 -> 51 | 6.1 | 4.3 | 1.8 |
| N | 109 | 85 -> 63 | 10.4 | 8.6 | 1.8 |
| NE | 4 | 3 -> 2 | 5.7 | 3.3 | 2.4 |
| NW | 93 | 73 -> 57 | 9.8 | 8.2 | 1.6 |
| S | 131 | 119 -> 88 | 5.7 | 3.6 | 2.1 |
| SE | 197 | 157 -> 130 | 8.5 | 6.8 | 1.6 |
| SW | 207 | 186 -> 149 | 4.7 | 4.0 | 0.7 |
| W | 140 | 116 -> 93 | 7.0 | 4.9 | 2.0 |
| 0-5 km | 71 | 70 -> 61 | 2.2 | 1.3 | 0.9 |
| 5-10 km | 316 | 286 -> 223 | 4.9 | 3.5 | 1.4 |
| 10-15 km | 215 | 187 -> 143 | 7.0 | 5.5 | 1.5 |
| 15-20 km | 161 | 128 -> 102 | 9.5 | 7.9 | 1.6 |
| 20-30 km | 172 | 118 -> 96 | 12.3 | 9.9 | 2.4 |
| 30+ km | 15 | 11 -> 8 | 11.7 | 8.4 | 3.3 |

### Home SA2s with the largest saving per trip (at least 8 commuters)

| SA2 | commuters | delay no charge | with charge | minutes saved |
|---|---|---|---|---|
| Whenuapai | 8 | 13.3 | 7.9 | 5.4 |
| Kumeu Rural East | 18 | 9.7 | 4.8 | 4.9 |
| Epsom Central-South | 16 | 6.1 | 2.3 | 3.7 |
| Westmere North | 14 | 6.3 | 3.3 | 2.9 |
| Okura Bush | 27 | 13.0 | 10.9 | 2.1 |
| Herne Bay | 11 | 3.7 | 2.2 | 1.5 |
| Sandringham North | 9 | 4.5 | 3.2 | 1.3 |
| Mount Eden West | 14 | 3.5 | 2.3 | 1.2 |
| Point Chevalier East | 15 | 4.5 | 3.5 | 1.1 |
| Grey Lynn North | 10 | 3.2 | 2.4 | 0.9 |

## R-clock_mock_py_s1 vs R-clock_mock_py_s1_peak0

- Commuter car trips per day: 812 without the charge, 625 with it.
- Delay per remaining car trip (road + gate queue): 8.1 -> 5.9 min (mean over drivers; door to door 19.6 -> 17.5 min).
- All vehicles on the simulated roads, 06:00-10:00: 29,183 vehicle-hours of delay per morning without the charge, 1,458 fewer with it (5.0%).

### Roads with the largest total saving (vehicle-hours of delay per morning, 06:00-10:00)

Per car: delay over the street's simulated sections, 07:00-09:00, weighted by traffic.

| street | motorway | km | delay per car, no charge (min) | with charge | minutes saved per car | % cut | vehicle-hours saved | % of street's delay |
|---|---|---|---|---|---|---|---|---|
| Northwestern Motorway | yes | 25.1 | 17.45 | 17.18 | 0.27 | 2% | 107 | 3% |
| Northern Motorway | yes | 25.4 | 19.87 | 19.87 | 0.00 | 0% | 98 | 2% |
| Mount Eden Road |  | 4.9 | 6.31 | 3.66 | 2.64 | 42% | 74 | 41% |
| Southwestern Motorway | yes | 18.5 | 2.39 | 1.82 | 0.57 | 24% | 74 | 18% |
| Dominion Road |  | 6.1 | 6.39 | 4.94 | 1.45 | 23% | 68 | 25% |
| Manukau Road |  | 4.1 | 4.02 | 2.76 | 1.26 | 31% | 56 | 36% |
| Tamaki Drive |  | 9.7 | 9.55 | 8.14 | 1.41 | 15% | 50 | 17% |
| Great North Road |  | 12.4 | 9.26 | 8.20 | 1.07 | 11% | 37 | 8% |
| Pakuranga Road |  | 6.2 | 4.04 | 3.70 | 0.34 | 8% | 31 | 8% |
| Entry 429 Wellesley Street |  | 0.7 | 0.94 | 0.52 | 0.42 | 44% | 31 | 51% |
| Entry 424 Fanshawe Street |  | 0.6 | 0.66 | 0.27 | 0.40 | 60% | 30 | 58% |
| Sandringham Road |  | 3.4 | 4.24 | 3.33 | 0.91 | 22% | 30 | 22% |

### Roads where delay grew (vehicle-hours per morning)

| street | km | vehicle-hours added | minutes per car 07:00-09:00, no charge -> charge |
|---|---|---|---|
| Southern Motorway | 41.9 | 160 | 28.84 -> 28.88 |
| East Coast Road | 5.0 | 2 | 3.02 -> 2.21 |
| Deep Creek Road | 1.7 | 1 | 1.17 -> 1.21 |
| Stanley Road | 1.1 | 0 | 0.67 -> 0.69 |
| Beach Haven Road | 1.5 | 0 | 1.04 -> 1.06 |

### Roads with the largest saving per car (at least 1 km simulated)

| street | km | delay per car, no charge (min) | with charge | minutes saved per car | % cut |
|---|---|---|---|---|---|
| Mount Eden Road | 4.9 | 6.31 | 3.66 | 2.64 | 42% |
| Dominion Road | 6.1 | 6.39 | 4.94 | 1.45 | 23% |
| Tamaki Drive | 9.7 | 9.55 | 8.14 | 1.41 | 15% |
| Manukau Road | 4.1 | 4.02 | 2.76 | 1.26 | 31% |
| Great North Road | 12.4 | 9.26 | 8.20 | 1.07 | 11% |
| Sandringham Road | 3.4 | 4.24 | 3.33 | 0.91 | 22% |
| Chivalry Road | 1.6 | 2.44 | 1.56 | 0.88 | 36% |
| East Coast Road | 5.0 | 3.02 | 2.21 | 0.81 | 27% |
| Onehunga Mall | 1.8 | 2.17 | 1.36 | 0.81 | 37% |
| Great South Road | 9.3 | 6.73 | 5.99 | 0.74 | 11% |

### By road region

| region | km | vehicle-hours saved (06-10) | % of its delay | per km | mean V/C 07-09, no charge -> charge | LoS E/F by speed 07-09 |
|---|---|---|---|---|---|---|
| Other roads | 368 | 1,022 | 9.3% | 2.8 | 1.37 -> 1.34 | 8% -> 5% |
| North Shore | 64 | 136 | 7.1% | 2.1 | 1.39 -> 1.37 | 12% -> 12% |
| SH16 | 25 | 107 | 2.7% | 4.2 | 0.85 -> 0.82 | 83% -> 81% |
| Green Lane | 11 | 105 | 26.1% | 9.6 | 1.39 -> 1.33 | 5% -> 1% |
| SH20 | 19 | 83 | 19.2% | 4.3 | 0.94 -> 0.93 | 7% -> 4% |
| New Lynn | 24 | 67 | 9.4% | 2.8 | 1.40 -> 1.38 | 10% -> 9% |
| SH1 | 67 | -61 | -0.6% | -0.9 | 0.86 -> 0.83 | 96% -> 96% |

### By where commuters live (delay per remaining car trip, min)

| group | commuters | car trips/day no charge -> charge | delay no charge | with charge | minutes saved |
|---|---|---|---|---|---|
| E | 69 | 62 -> 50 | 6.4 | 4.7 | 1.7 |
| N | 109 | 86 -> 64 | 10.6 | 9.1 | 1.5 |
| NE | 4 | 3 -> 2 | 8.7 | 4.0 | 4.7 |
| NW | 93 | 75 -> 56 | 10.2 | 8.8 | 1.5 |
| S | 131 | 122 -> 86 | 7.1 | 3.8 | 3.3 |
| SE | 197 | 160 -> 127 | 9.6 | 7.2 | 2.4 |
| SW | 207 | 188 -> 148 | 5.9 | 4.3 | 1.6 |
| W | 140 | 116 -> 92 | 7.9 | 5.2 | 2.7 |
| 0-5 km | 71 | 70 -> 59 | 2.8 | 1.8 | 1.0 |
| 5-10 km | 316 | 292 -> 220 | 5.9 | 3.9 | 2.1 |
| 10-15 km | 215 | 188 -> 140 | 7.9 | 5.9 | 2.0 |
| 15-20 km | 161 | 131 -> 103 | 10.5 | 8.0 | 2.5 |
| 20-30 km | 172 | 120 -> 95 | 12.9 | 10.3 | 2.6 |
| 30+ km | 15 | 11 -> 8 | 18.0 | 11.7 | 6.3 |

### Home SA2s with the largest saving per trip (at least 8 commuters)

| SA2 | commuters | delay no charge | with charge | minutes saved |
|---|---|---|---|---|
| Kumeu Rural East | 18 | 12.5 | 5.0 | 7.5 |
| Mount Eden West | 14 | 7.0 | 2.7 | 4.3 |
| Whenuapai | 8 | 12.9 | 9.6 | 3.3 |
| Epsom Central-South | 16 | 5.8 | 2.8 | 3.0 |
| Westmere North | 14 | 7.0 | 4.6 | 2.4 |
| Point Chevalier East | 15 | 5.8 | 3.5 | 2.3 |
| Grey Lynn North | 10 | 4.9 | 2.7 | 2.2 |
| Okura Bush | 27 | 13.7 | 11.9 | 1.9 |
| Sandringham North | 9 | 4.1 | 2.8 | 1.4 |
| Herne Bay | 11 | 3.9 | 2.8 | 1.1 |

