# Where and when the charge relieves congestion: rule (R-clock) and LLM (H-clock)

Before = days 2-5, charge = days 6-10; daily means. Vehicle-hours: all vehicles on the simulated roads (background traffic and commuters), 06:00-10:00, from road_los.csv hour means.

## Summary

| scenario | arm | car_share | pt_share | wfh_share | cars_peak_hour_change_pct | cars_other_hours_change_pct | road_delay_per_car | queue_per_car | veh_h_all_roads_before | veh_h_all_roads_change_pct | veh_h_motorway_change_pct | veh_h_other_roads_change_pct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NZ6_s1 | H-clock | 0.847 -> 0.559 | 0.153 -> 0.405 | 0.000 -> 0.036 | -48.0 | -22.3 | 6.527 -> 5.398 | 1.473 -> 0.270 | 26448.2 | -5.7 | -2.8 | -9.6 |
| NZ6_s1 | R-clock | 0.855 -> 0.658 | 0.145 -> 0.326 | 0.000 -> 0.016 | -53.7 | 2.2 | 6.555 -> 5.133 | 1.517 -> 0.754 | 26470.1 | -4.5 | -1.3 | -8.9 |
| NZ6_s2 | H-clock | 0.825 -> 0.534 | 0.175 -> 0.435 | 0.000 -> 0.030 | -46.7 | -25.3 | 7.106 -> 5.841 | 1.662 -> 0.175 | 26520.4 | -6.3 | -3.5 | -10.1 |
| NZ6_s2 | R-clock | 0.845 -> 0.633 | 0.155 -> 0.343 | 0.000 -> 0.024 | -54.0 | -1.5 | 7.133 -> 5.335 | 2.049 -> 0.422 | 26558.9 | -5.3 | -2.4 | -9.3 |
| NZ6_s3 | H-clock | 0.845 -> 0.550 | 0.154 -> 0.419 | 0.001 -> 0.032 | -50.5 | -21.4 | 7.348 -> 5.972 | 1.351 -> 0.141 | 26798.7 | -6.5 | -3.5 | -10.7 |
| NZ6_s3 | R-clock | 0.860 -> 0.642 | 0.140 -> 0.332 | 0.000 -> 0.026 | -57.1 | 2.5 | 7.448 -> 5.557 | 1.602 -> 0.349 | 26874.4 | -6.3 | -3.4 | -10.4 |
| NZ18_s1 | H-clock | 0.847 -> 0.251 | 0.153 -> 0.710 | 0.000 -> 0.039 | -85.3 | -58.0 | 6.527 -> 4.664 | 1.473 -> 0.091 | 26448.2 | -10.2 | -5.8 | -16.2 |
| NZ18_s1 | R-clock | 0.855 -> 0.323 | 0.145 -> 0.553 | 0.000 -> 0.124 | -89.1 | -40.0 | 6.555 -> 3.941 | 1.517 -> 0.238 | 26470.1 | -10.1 | -5.7 | -16.2 |

## by region

| scenario | arm | region | km | veh_h_before | veh_h_change | veh_h_change_pct | vc_mean_0709_before | vc_mean_0709_charge |
|---|---|---|---|---|---|---|---|---|
| NZ6_s1 | H-clock | Green Lane | 10.94 | 350.65 | -63.69 | -18.16 | 1.40 | 1.35 |
| NZ6_s1 | H-clock | New Lynn | 23.89 | 604.68 | -32.79 | -5.42 | 1.41 | 1.39 |
| NZ6_s1 | H-clock | North Shore | 63.63 | 1738.52 | -159.94 | -9.20 | 1.40 | 1.37 |
| NZ6_s1 | H-clock | Other roads | 368.14 | 9952.05 | -825.97 | -8.30 | 1.34 | 1.32 |
| NZ6_s1 | H-clock | SH1 | 67.26 | 9964.69 | -285.23 | -2.86 | 0.84 | 0.82 |
| NZ6_s1 | H-clock | SH16 | 25.14 | 3500.31 | -109.04 | -3.12 | 0.82 | 0.79 |
| NZ6_s1 | H-clock | SH20 | 19.23 | 337.31 | -27.06 | -8.02 | 0.93 | 0.93 |
| NZ6_s1 | R-clock | Green Lane | 10.94 | 354.21 | -87.17 | -24.61 | 1.41 | 1.33 |
| NZ6_s1 | R-clock | New Lynn | 23.89 | 603.87 | -35.48 | -5.88 | 1.41 | 1.39 |
| NZ6_s1 | R-clock | North Shore | 63.63 | 1737.05 | -113.66 | -6.54 | 1.40 | 1.38 |
| NZ6_s1 | R-clock | Other roads | 368.14 | 9956.31 | -775.00 | -7.78 | 1.35 | 1.32 |
| NZ6_s1 | R-clock | SH1 | 67.26 | 9971.74 | -48.79 | -0.49 | 0.85 | 0.82 |
| NZ6_s1 | R-clock | SH16 | 25.14 | 3506.31 | -102.76 | -2.93 | 0.82 | 0.79 |
| NZ6_s1 | R-clock | SH20 | 19.23 | 340.64 | -35.34 | -10.37 | 0.93 | 0.93 |
| NZ6_s2 | H-clock | Green Lane | 10.59 | 287.28 | -29.74 | -10.35 | 1.36 | 1.33 |
| NZ6_s2 | H-clock | New Lynn | 23.45 | 621.53 | -58.31 | -9.38 | 1.42 | 1.39 |
| NZ6_s2 | H-clock | North Shore | 67.64 | 1953.22 | -216.11 | -11.06 | 1.42 | 1.38 |
| NZ6_s2 | H-clock | Other roads | 369.37 | 9613.41 | -864.91 | -9.00 | 1.34 | 1.31 |
| NZ6_s2 | H-clock | SH1 | 67.58 | 10133.48 | -296.66 | -2.93 | 0.84 | 0.82 |
| NZ6_s2 | H-clock | SH16 | 25.14 | 3542.93 | -130.92 | -3.70 | 0.83 | 0.80 |
| NZ6_s2 | H-clock | SH20 | 15.27 | 368.58 | -67.82 | -18.40 | 0.94 | 0.93 |
| NZ6_s2 | R-clock | Green Lane | 10.59 | 289.31 | -26.98 | -9.33 | 1.36 | 1.34 |
| NZ6_s2 | R-clock | New Lynn | 23.45 | 621.51 | -71.05 | -11.43 | 1.42 | 1.37 |
| NZ6_s2 | R-clock | North Shore | 67.64 | 1957.13 | -211.78 | -10.82 | 1.42 | 1.39 |
| NZ6_s2 | R-clock | Other roads | 369.37 | 9597.98 | -770.86 | -8.03 | 1.35 | 1.32 |
| NZ6_s2 | R-clock | SH1 | 67.58 | 10168.50 | -145.29 | -1.43 | 0.84 | 0.82 |
| NZ6_s2 | R-clock | SH16 | 25.14 | 3547.76 | -110.93 | -3.13 | 0.84 | 0.79 |
| NZ6_s2 | R-clock | SH20 | 15.27 | 376.72 | -82.47 | -21.89 | 0.94 | 0.93 |
| NZ6_s3 | H-clock | Green Lane | 10.02 | 320.10 | -55.38 | -17.30 | 1.39 | 1.35 |
| NZ6_s3 | H-clock | New Lynn | 21.43 | 632.29 | -90.40 | -14.30 | 1.44 | 1.40 |
| NZ6_s3 | H-clock | North Shore | 64.36 | 1844.59 | -199.26 | -10.80 | 1.41 | 1.38 |
| NZ6_s3 | H-clock | Other roads | 371.64 | 9892.21 | -858.94 | -8.68 | 1.34 | 1.31 |
| NZ6_s3 | H-clock | SH1 | 67.26 | 10107.13 | -296.86 | -2.94 | 0.84 | 0.82 |
| NZ6_s3 | H-clock | SH16 | 25.14 | 3558.90 | -162.30 | -4.56 | 0.84 | 0.79 |
| NZ6_s3 | H-clock | SH20 | 17.84 | 443.45 | -74.76 | -16.86 | 0.94 | 0.93 |
| NZ6_s3 | R-clock | Green Lane | 10.02 | 319.77 | -52.51 | -16.42 | 1.40 | 1.36 |
| NZ6_s3 | R-clock | New Lynn | 21.43 | 636.99 | -149.96 | -23.54 | 1.44 | 1.36 |
| NZ6_s3 | R-clock | North Shore | 64.36 | 1847.60 | -182.02 | -9.85 | 1.41 | 1.39 |
| NZ6_s3 | R-clock | Other roads | 371.64 | 9939.13 | -795.74 | -8.01 | 1.34 | 1.32 |
| NZ6_s3 | R-clock | SH1 | 67.26 | 10119.60 | -293.51 | -2.90 | 0.85 | 0.82 |
| NZ6_s3 | R-clock | SH16 | 25.14 | 3565.81 | -107.18 | -3.01 | 0.84 | 0.80 |
| NZ6_s3 | R-clock | SH20 | 17.84 | 445.48 | -112.90 | -25.34 | 0.95 | 0.93 |
| NZ18_s1 | H-clock | Green Lane | 10.94 | 350.65 | -108.32 | -30.89 | 1.40 | 1.30 |
| NZ18_s1 | H-clock | New Lynn | 23.89 | 604.68 | -101.62 | -16.81 | 1.41 | 1.33 |
| NZ18_s1 | H-clock | North Shore | 63.63 | 1738.52 | -216.71 | -12.47 | 1.40 | 1.36 |
| NZ18_s1 | H-clock | Other roads | 368.14 | 9952.05 | -1413.17 | -14.20 | 1.34 | 1.29 |
| NZ18_s1 | H-clock | SH1 | 67.26 | 9964.69 | -531.29 | -5.33 | 0.84 | 0.80 |
| NZ18_s1 | H-clock | SH16 | 25.14 | 3500.31 | -241.21 | -6.89 | 0.82 | 0.76 |
| NZ18_s1 | H-clock | SH20 | 19.23 | 337.31 | -80.41 | -23.84 | 0.93 | 0.92 |
| NZ18_s1 | R-clock | Green Lane | 10.94 | 354.21 | -116.71 | -32.95 | 1.41 | 1.30 |
| NZ18_s1 | R-clock | New Lynn | 23.89 | 603.87 | -96.94 | -16.05 | 1.41 | 1.34 |
| NZ18_s1 | R-clock | North Shore | 63.63 | 1737.05 | -226.73 | -13.05 | 1.40 | 1.35 |
| NZ18_s1 | R-clock | Other roads | 368.14 | 9956.31 | -1399.40 | -14.06 | 1.35 | 1.29 |
| NZ18_s1 | R-clock | SH1 | 67.26 | 9971.74 | -516.92 | -5.18 | 0.85 | 0.79 |
| NZ18_s1 | R-clock | SH16 | 25.14 | 3506.31 | -233.42 | -6.66 | 0.82 | 0.76 |
| NZ18_s1 | R-clock | SH20 | 19.23 | 340.64 | -86.67 | -25.44 | 0.93 | 0.92 |

## by corridor

| scenario | arm | corridor | car_trips_before | car_trips_charge | road_delay_per_trip_before | road_delay_per_trip_charge | queue_per_trip_before | queue_per_trip_charge | delay_per_trip_change_min |
|---|---|---|---|---|---|---|---|---|---|
| NZ6_s1 | H-clock | East | 46.25 | 27.60 | 4.28 | 1.82 | 0.14 | 0.11 | -2.49 |
| NZ6_s1 | H-clock | South-east | 183.00 | 119.40 | 7.12 | 5.42 | 1.20 | 0.11 | -2.79 |
| NZ6_s1 | H-clock | South | 90.50 | 66.20 | 7.54 | 6.59 | 2.07 | 0.64 | -2.39 |
| NZ6_s1 | H-clock | South-west | 291.25 | 199.20 | 5.29 | 4.56 | 1.57 | 0.28 | -2.03 |
| NZ6_s1 | H-clock | West | 193.75 | 119.00 | 7.89 | 6.95 | 1.62 | 0.26 | -2.30 |
| NZ6_s1 | R-clock | East | 47.00 | 38.00 | 4.47 | 3.05 | 0.15 | 0.16 | -1.41 |
| NZ6_s1 | R-clock | South-east | 183.00 | 141.00 | 7.10 | 5.44 | 1.10 | 0.57 | -2.19 |
| NZ6_s1 | R-clock | South | 92.00 | 67.00 | 7.73 | 5.36 | 2.41 | 1.33 | -3.45 |
| NZ6_s1 | R-clock | South-west | 294.00 | 230.00 | 5.33 | 4.30 | 1.63 | 0.54 | -2.11 |
| NZ6_s1 | R-clock | West | 196.00 | 149.00 | 7.84 | 6.55 | 1.65 | 1.15 | -1.78 |
| NZ6_s2 | H-clock | East | 55.00 | 36.80 | 5.15 | 3.01 | 0.15 | 0.09 | -2.20 |
| NZ6_s2 | H-clock | South-east | 128.25 | 76.80 | 7.33 | 5.20 | 4.38 | 0.22 | -6.30 |
| NZ6_s2 | H-clock | South | 90.00 | 65.00 | 8.17 | 7.03 | 1.11 | 0.42 | -1.83 |
| NZ6_s2 | H-clock | South-west | 296.75 | 193.80 | 6.29 | 5.50 | 1.36 | 0.10 | -2.05 |
| NZ6_s2 | H-clock | West | 213.75 | 135.20 | 8.16 | 6.90 | 1.07 | 0.17 | -2.17 |
| NZ6_s2 | R-clock | East | 54.00 | 45.00 | 4.91 | 3.50 | 0.13 | 0.25 | -1.29 |
| NZ6_s2 | R-clock | South-east | 145.50 | 114.00 | 7.48 | 4.74 | 4.80 | 1.18 | -6.37 |
| NZ6_s2 | R-clock | South | 90.00 | 76.00 | 8.03 | 6.50 | 0.87 | 0.34 | -2.06 |
| NZ6_s2 | R-clock | South-west | 298.25 | 215.00 | 6.31 | 4.46 | 1.90 | 0.22 | -3.54 |
| NZ6_s2 | R-clock | West | 215.00 | 151.00 | 8.22 | 7.00 | 1.36 | 0.23 | -2.36 |
| NZ6_s3 | H-clock | East | 51.25 | 34.00 | 5.66 | 4.12 | 0.29 | 0.15 | -1.69 |
| NZ6_s3 | H-clock | South-east | 154.75 | 96.20 | 7.64 | 5.08 | 1.05 | 0.09 | -3.53 |
| NZ6_s3 | H-clock | South | 97.50 | 75.00 | 8.07 | 7.59 | 0.75 | 0.33 | -0.90 |
| NZ6_s3 | H-clock | South-west | 308.25 | 201.00 | 6.54 | 5.32 | 1.76 | 0.06 | -2.93 |
| NZ6_s3 | H-clock | West | 191.25 | 116.20 | 8.49 | 7.34 | 1.53 | 0.21 | -2.47 |
| NZ6_s3 | R-clock | East | 52.00 | 42.00 | 5.90 | 3.98 | 0.31 | 0.26 | -1.97 |
| NZ6_s3 | R-clock | South-east | 160.00 | 120.00 | 7.88 | 4.97 | 1.60 | 0.23 | -4.28 |
| NZ6_s3 | R-clock | South | 98.00 | 77.00 | 8.09 | 6.53 | 0.67 | 0.79 | -1.44 |
| NZ6_s3 | R-clock | South-west | 315.00 | 230.00 | 6.62 | 4.56 | 2.29 | 0.33 | -4.01 |
| NZ6_s3 | R-clock | West | 192.25 | 141.00 | 8.54 | 7.62 | 1.31 | 0.26 | -1.97 |
| NZ18_s1 | H-clock | East | 46.25 | 12.60 | 4.28 | 1.41 | 0.14 | 0.08 | -2.92 |
| NZ18_s1 | H-clock | South-east | 183.00 | 53.60 | 7.12 | 4.53 | 1.20 | 0.03 | -3.76 |
| NZ18_s1 | H-clock | South | 90.50 | 29.40 | 7.54 | 5.06 | 2.07 | 0.42 | -4.13 |
| NZ18_s1 | H-clock | South-west | 291.25 | 87.20 | 5.29 | 3.84 | 1.57 | 0.01 | -3.01 |
| NZ18_s1 | H-clock | West | 193.75 | 55.80 | 7.89 | 6.60 | 1.62 | 0.10 | -2.81 |
| NZ18_s1 | R-clock | East | 47.00 | 15.00 | 4.47 | 0.87 | 0.15 | 0.07 | -3.68 |
| NZ18_s1 | R-clock | South-east | 183.00 | 76.00 | 7.10 | 4.11 | 1.10 | 0.16 | -3.94 |
| NZ18_s1 | R-clock | South | 92.00 | 33.00 | 7.73 | 3.73 | 2.41 | 0.42 | -5.99 |
| NZ18_s1 | R-clock | South-west | 294.00 | 116.00 | 5.33 | 3.24 | 1.63 | 0.27 | -3.45 |
| NZ18_s1 | R-clock | West | 196.00 | 67.00 | 7.84 | 5.76 | 1.65 | 0.22 | -3.50 |

## by home area

| scenario | arm | grouping | area | commuters | base_drivers | left_car_share | to_pt_share | delay_per_trip_before | delay_per_trip_charge | delay_per_trip_change_min |
|---|---|---|---|---|---|---|---|---|---|---|
| NZ6_s1 | H-clock | sector | E | 69.00 | 61.00 | 0.38 | 0.33 | 6.30 | 4.42 | -1.88 |
| NZ6_s1 | H-clock | sector | N | 110.00 | 86.00 | 0.43 | 0.38 | 10.51 | 7.76 | -2.75 |
| NZ6_s1 | H-clock | sector | NE | 4.00 | 3.00 | 0.33 | 0.33 | 8.42 | 4.50 | -3.92 |
| NZ6_s1 | H-clock | sector | NW | 92.00 | 73.00 | 0.36 | 0.30 | 10.57 | 9.07 | -1.50 |
| NZ6_s1 | H-clock | sector | S | 141.00 | 129.00 | 0.33 | 0.26 | 6.92 | 3.95 | -2.97 |
| NZ6_s1 | H-clock | sector | SE | 199.00 | 161.00 | 0.34 | 0.30 | 9.48 | 7.00 | -2.48 |
| NZ6_s1 | H-clock | sector | SW | 195.00 | 176.00 | 0.30 | 0.25 | 5.79 | 4.08 | -1.71 |
| NZ6_s1 | H-clock | sector | W | 140.00 | 113.00 | 0.34 | 0.29 | 7.90 | 5.54 | -2.36 |
| NZ6_s1 | H-clock | distance | 0-5 km | 210.00 | 202.00 | 0.35 | 0.30 | 4.60 | 2.06 | -2.54 |
| NZ6_s1 | H-clock | distance | 10-15 km | 224.00 | 186.00 | 0.32 | 0.27 | 10.50 | 8.39 | -2.11 |
| NZ6_s1 | H-clock | distance | 15-20 km | 123.00 | 90.00 | 0.39 | 0.34 | 12.43 | 8.85 | -3.59 |
| NZ6_s1 | H-clock | distance | 20-30 km | 40.00 | 19.00 | 0.11 | 0.11 | 15.87 | 13.42 | -2.45 |
| NZ6_s1 | H-clock | distance | 5-10 km | 353.00 | 305.00 | 0.35 | 0.30 | 6.92 | 4.79 | -2.14 |
| NZ6_s1 | R-clock | sector | E | 69.00 | 62.00 | 0.19 | 0.18 | 6.42 | 4.74 | -1.68 |
| NZ6_s1 | R-clock | sector | N | 110.00 | 87.00 | 0.25 | 0.24 | 10.60 | 9.07 | -1.54 |
| NZ6_s1 | R-clock | sector | NE | 4.00 | 3.00 | 0.33 | 0.33 | 8.67 | 4.00 | -4.67 |
| NZ6_s1 | R-clock | sector | NW | 92.00 | 74.00 | 0.26 | 0.23 | 10.39 | 8.84 | -1.55 |
| NZ6_s1 | R-clock | sector | S | 141.00 | 130.00 | 0.26 | 0.24 | 7.10 | 3.74 | -3.36 |
| NZ6_s1 | R-clock | sector | SE | 199.00 | 162.00 | 0.22 | 0.21 | 9.51 | 7.18 | -2.33 |
| NZ6_s1 | R-clock | sector | SW | 195.00 | 178.00 | 0.22 | 0.20 | 5.91 | 4.41 | -1.50 |
| NZ6_s1 | R-clock | sector | W | 140.00 | 116.00 | 0.21 | 0.19 | 7.95 | 5.20 | -2.76 |
| NZ6_s1 | R-clock | distance | 0-5 km | 210.00 | 203.00 | 0.23 | 0.22 | 4.54 | 2.62 | -1.93 |
| NZ6_s1 | R-clock | distance | 10-15 km | 224.00 | 187.00 | 0.20 | 0.18 | 10.53 | 8.07 | -2.46 |
| NZ6_s1 | R-clock | distance | 15-20 km | 123.00 | 91.00 | 0.25 | 0.25 | 12.56 | 9.74 | -2.82 |
| NZ6_s1 | R-clock | distance | 20-30 km | 40.00 | 20.00 | 0.20 | 0.20 | 16.62 | 12.69 | -3.94 |
| NZ6_s1 | R-clock | distance | 5-10 km | 353.00 | 311.00 | 0.24 | 0.22 | 7.04 | 5.10 | -1.94 |
| NZ6_s2 | H-clock | sector | E | 67.00 | 55.00 | 0.33 | 0.31 | 5.85 | 3.42 | -2.43 |
| NZ6_s2 | H-clock | sector | N | 117.00 | 96.00 | 0.43 | 0.38 | 10.50 | 8.77 | -1.73 |
| NZ6_s2 | H-clock | sector | NE | 7.00 | 6.00 | 0.17 | 0.00 | 6.67 | 5.85 | -0.82 |
| NZ6_s2 | H-clock | sector | NW | 100.00 | 79.00 | 0.34 | 0.30 | 10.47 | 7.67 | -2.81 |
| NZ6_s2 | H-clock | sector | S | 97.00 | 83.00 | 0.33 | 0.28 | 6.63 | 3.48 | -3.15 |
| NZ6_s2 | H-clock | sector | SE | 202.00 | 144.00 | 0.33 | 0.31 | 12.14 | 7.51 | -4.64 |
| NZ6_s2 | H-clock | sector | SW | 199.00 | 172.00 | 0.37 | 0.31 | 6.01 | 3.98 | -2.03 |
| NZ6_s2 | H-clock | sector | W | 161.00 | 137.00 | 0.31 | 0.28 | 8.93 | 6.83 | -2.10 |
| NZ6_s2 | H-clock | distance | 0-5 km | 189.00 | 173.00 | 0.34 | 0.29 | 5.00 | 2.07 | -2.93 |
| NZ6_s2 | H-clock | distance | 10-15 km | 244.00 | 196.00 | 0.34 | 0.30 | 10.68 | 8.27 | -2.41 |
| NZ6_s2 | H-clock | distance | 15-20 km | 130.00 | 88.00 | 0.32 | 0.28 | 13.52 | 9.76 | -3.76 |
| NZ6_s2 | H-clock | distance | 20-30 km | 41.00 | 32.00 | 0.28 | 0.28 | 15.30 | 11.16 | -4.14 |
| NZ6_s2 | H-clock | distance | 5-10 km | 346.00 | 283.00 | 0.38 | 0.34 | 7.56 | 4.99 | -2.57 |
| NZ6_s2 | R-clock | sector | E | 67.00 | 54.00 | 0.20 | 0.19 | 5.47 | 3.90 | -1.57 |
| NZ6_s2 | R-clock | sector | N | 117.00 | 96.00 | 0.33 | 0.29 | 10.76 | 8.52 | -2.24 |
| NZ6_s2 | R-clock | sector | NE | 7.00 | 6.00 | 0.17 | 0.00 | 6.50 | 5.60 | -0.90 |
| NZ6_s2 | R-clock | sector | NW | 100.00 | 81.00 | 0.28 | 0.23 | 10.94 | 8.17 | -2.77 |
| NZ6_s2 | R-clock | sector | S | 97.00 | 90.00 | 0.17 | 0.14 | 7.49 | 3.38 | -4.11 |
| NZ6_s2 | R-clock | sector | SE | 202.00 | 163.00 | 0.20 | 0.18 | 12.16 | 7.38 | -4.77 |
| NZ6_s2 | R-clock | sector | SW | 199.00 | 173.00 | 0.26 | 0.23 | 6.63 | 3.74 | -2.89 |
| NZ6_s2 | R-clock | sector | W | 161.00 | 139.00 | 0.30 | 0.28 | 9.41 | 5.62 | -3.79 |
| NZ6_s2 | R-clock | distance | 0-5 km | 189.00 | 180.00 | 0.23 | 0.20 | 5.58 | 2.24 | -3.34 |
| NZ6_s2 | R-clock | distance | 10-15 km | 244.00 | 201.00 | 0.28 | 0.25 | 10.97 | 7.66 | -3.31 |
| NZ6_s2 | R-clock | distance | 15-20 km | 130.00 | 92.00 | 0.32 | 0.28 | 14.03 | 9.61 | -4.43 |
| NZ6_s2 | R-clock | distance | 20-30 km | 41.00 | 32.00 | 0.12 | 0.12 | 15.15 | 10.46 | -4.68 |
| NZ6_s2 | R-clock | distance | 5-10 km | 346.00 | 297.00 | 0.24 | 0.21 | 8.01 | 5.05 | -2.96 |
| NZ6_s3 | H-clock | sector | E | 74.00 | 64.00 | 0.34 | 0.31 | 6.82 | 4.71 | -2.11 |
| NZ6_s3 | H-clock | sector | N | 109.00 | 92.00 | 0.45 | 0.38 | 10.91 | 8.82 | -2.09 |
| NZ6_s3 | H-clock | sector | NE | 10.00 | 9.00 | 0.56 | 0.56 | 12.89 | 7.50 | -5.39 |
| NZ6_s3 | H-clock | sector | NW | 97.00 | 74.00 | 0.32 | 0.30 | 10.07 | 7.52 | -2.55 |
| NZ6_s3 | H-clock | sector | S | 128.00 | 114.00 | 0.33 | 0.28 | 6.29 | 3.75 | -2.54 |
| NZ6_s3 | H-clock | sector | SE | 197.00 | 151.00 | 0.32 | 0.28 | 9.87 | 7.59 | -2.29 |
| NZ6_s3 | H-clock | sector | SW | 199.00 | 174.00 | 0.32 | 0.26 | 8.14 | 5.14 | -3.00 |
| NZ6_s3 | H-clock | sector | W | 136.00 | 118.00 | 0.38 | 0.37 | 8.50 | 5.93 | -2.57 |
| NZ6_s3 | H-clock | distance | 0-5 km | 173.00 | 155.00 | 0.36 | 0.32 | 4.91 | 2.20 | -2.72 |
| NZ6_s3 | H-clock | distance | 10-15 km | 260.00 | 209.00 | 0.33 | 0.30 | 10.86 | 7.72 | -3.14 |
| NZ6_s3 | H-clock | distance | 15-20 km | 128.00 | 96.00 | 0.31 | 0.30 | 12.07 | 8.92 | -3.14 |
| NZ6_s3 | H-clock | distance | 20-30 km | 50.00 | 33.00 | 0.24 | 0.21 | 13.76 | 13.41 | -0.35 |
| NZ6_s3 | H-clock | distance | 5-10 km | 339.00 | 303.00 | 0.38 | 0.32 | 7.52 | 5.03 | -2.49 |
| NZ6_s3 | R-clock | sector | E | 74.00 | 65.00 | 0.20 | 0.15 | 7.07 | 4.63 | -2.43 |
| NZ6_s3 | R-clock | sector | N | 109.00 | 93.00 | 0.27 | 0.22 | 10.75 | 9.22 | -1.52 |
| NZ6_s3 | R-clock | sector | NE | 10.00 | 9.00 | 0.67 | 0.56 | 12.61 | 8.00 | -4.61 |
| NZ6_s3 | R-clock | sector | NW | 97.00 | 75.00 | 0.24 | 0.24 | 9.92 | 7.78 | -2.14 |
| NZ6_s3 | R-clock | sector | S | 128.00 | 120.00 | 0.22 | 0.20 | 6.75 | 3.49 | -3.26 |
| NZ6_s3 | R-clock | sector | SE | 197.00 | 155.00 | 0.26 | 0.24 | 10.44 | 7.35 | -3.09 |
| NZ6_s3 | R-clock | sector | SW | 199.00 | 182.00 | 0.29 | 0.24 | 8.82 | 4.26 | -4.57 |
| NZ6_s3 | R-clock | sector | W | 136.00 | 118.00 | 0.22 | 0.21 | 8.84 | 5.93 | -2.91 |
| NZ6_s3 | R-clock | distance | 0-5 km | 173.00 | 158.00 | 0.24 | 0.23 | 5.35 | 2.07 | -3.29 |
| NZ6_s3 | R-clock | distance | 10-15 km | 260.00 | 218.00 | 0.28 | 0.24 | 11.12 | 7.27 | -3.85 |
| NZ6_s3 | R-clock | distance | 15-20 km | 128.00 | 97.00 | 0.24 | 0.22 | 12.38 | 10.16 | -2.22 |
| NZ6_s3 | R-clock | distance | 20-30 km | 50.00 | 33.00 | 0.27 | 0.27 | 13.82 | 12.25 | -1.57 |
| NZ6_s3 | R-clock | distance | 5-10 km | 339.00 | 311.00 | 0.24 | 0.20 | 7.93 | 4.97 | -2.96 |
| NZ18_s1 | H-clock | sector | E | 69.00 | 61.00 | 0.74 | 0.72 | 6.30 | 3.10 | -3.20 |
| NZ18_s1 | H-clock | sector | N | 110.00 | 86.00 | 0.72 | 0.71 | 10.51 | 7.33 | -3.18 |
| NZ18_s1 | H-clock | sector | NE | 4.00 | 3.00 | 0.33 | 0.33 | 8.42 | 2.89 | -5.53 |
| NZ18_s1 | H-clock | sector | NW | 92.00 | 73.00 | 0.68 | 0.66 | 10.57 | 7.85 | -2.71 |
| NZ18_s1 | H-clock | sector | S | 141.00 | 129.00 | 0.74 | 0.66 | 6.92 | 2.86 | -4.06 |
| NZ18_s1 | H-clock | sector | SE | 199.00 | 161.00 | 0.67 | 0.61 | 9.48 | 5.46 | -4.03 |
| NZ18_s1 | H-clock | sector | SW | 195.00 | 176.00 | 0.70 | 0.65 | 5.79 | 3.31 | -2.48 |
| NZ18_s1 | H-clock | sector | W | 140.00 | 113.00 | 0.72 | 0.65 | 7.90 | 4.79 | -3.11 |
| NZ18_s1 | H-clock | distance | 0-5 km | 210.00 | 202.00 | 0.77 | 0.74 | 4.60 | 1.58 | -3.02 |
| NZ18_s1 | H-clock | distance | 10-15 km | 224.00 | 186.00 | 0.67 | 0.60 | 10.50 | 6.56 | -3.94 |
| NZ18_s1 | H-clock | distance | 15-20 km | 123.00 | 90.00 | 0.69 | 0.64 | 12.43 | 7.15 | -5.28 |
| NZ18_s1 | H-clock | distance | 20-30 km | 40.00 | 19.00 | 0.53 | 0.42 | 15.87 | 9.30 | -6.57 |
| NZ18_s1 | H-clock | distance | 5-10 km | 353.00 | 305.00 | 0.70 | 0.65 | 6.92 | 3.93 | -2.99 |
| NZ18_s1 | R-clock | sector | E | 69.00 | 62.00 | 0.66 | 0.50 | 6.42 | 2.19 | -4.23 |
| NZ18_s1 | R-clock | sector | N | 110.00 | 87.00 | 0.69 | 0.54 | 10.60 | 7.11 | -3.49 |
| NZ18_s1 | R-clock | sector | NE | 4.00 | 3.00 | 0.67 | 0.33 | 8.67 | 2.00 | -6.67 |
| NZ18_s1 | R-clock | sector | NW | 92.00 | 74.00 | 0.62 | 0.50 | 10.39 | 6.61 | -3.78 |
| NZ18_s1 | R-clock | sector | S | 141.00 | 130.00 | 0.62 | 0.43 | 7.10 | 2.64 | -4.46 |
| NZ18_s1 | R-clock | sector | SE | 199.00 | 162.00 | 0.60 | 0.48 | 9.51 | 5.02 | -4.50 |
| NZ18_s1 | R-clock | sector | SW | 195.00 | 178.00 | 0.59 | 0.44 | 5.91 | 3.18 | -2.73 |
| NZ18_s1 | R-clock | sector | W | 140.00 | 116.00 | 0.63 | 0.50 | 7.95 | 4.02 | -3.93 |
| NZ18_s1 | R-clock | distance | 0-5 km | 210.00 | 203.00 | 0.60 | 0.49 | 4.54 | 1.61 | -2.93 |
| NZ18_s1 | R-clock | distance | 10-15 km | 224.00 | 187.00 | 0.58 | 0.44 | 10.53 | 5.90 | -4.63 |
| NZ18_s1 | R-clock | distance | 15-20 km | 123.00 | 91.00 | 0.74 | 0.60 | 12.56 | 7.75 | -4.81 |
| NZ18_s1 | R-clock | distance | 20-30 km | 40.00 | 20.00 | 0.60 | 0.45 | 16.62 | 6.88 | -9.75 |
| NZ18_s1 | R-clock | distance | 5-10 km | 353.00 | 311.00 | 0.63 | 0.46 | 7.04 | 3.89 | -3.14 |

## streets with the largest change (at least 40 vehicle-hours of delay before the charge)

### NZ6_s1, H-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Southern Motorway | 41.89 | 5582.37 | -143.96 | 27.38 | 27.30 |
| Northern Motorway | 25.38 | 4382.33 | -141.27 | 19.87 | 19.87 |
| Northwestern Motorway | 25.14 | 3500.31 | -109.04 | 16.59 | 16.38 |
| Dominion Road | 6.14 | 243.95 | -71.13 | 5.77 | 4.31 |
| Tamaki Drive | 9.74 | 267.19 | -58.88 | 8.51 | 6.91 |
| Mount Eden Road | 4.95 | 145.94 | -40.19 | 5.09 | 3.80 |
| Manukau Road | 4.14 | 132.07 | -39.07 | 3.52 | 2.58 |
| Entry 429 Wellesley Street | 0.74 | 48.77 | -35.57 | 0.77 | 0.27 |
| East Coast Road | 4.95 | 73.57 | -24.54 | 2.57 | 1.65 |
| Kepa Road | 2.38 | 64.72 | -24.05 | 1.51 | 0.93 |
| Sandringham Road | 3.40 | 101.58 | -23.98 | 3.00 | 2.35 |
| Southwestern Motorway | 18.48 | 322.89 | -23.17 | 1.77 | 1.58 |

### NZ6_s1, R-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Northern Motorway | 25.38 | 4384.18 | -103.37 | 19.87 | 19.87 |
| Northwestern Motorway | 25.14 | 3506.31 | -102.76 | 16.59 | 16.38 |
| Dominion Road | 6.14 | 241.27 | -62.16 | 5.71 | 4.36 |
| Mount Eden Road | 4.95 | 145.56 | -51.65 | 5.08 | 3.33 |
| Manukau Road | 4.14 | 132.61 | -50.86 | 3.54 | 2.29 |
| Tamaki Drive | 9.74 | 269.11 | -34.03 | 8.55 | 7.69 |
| Southwestern Motorway | 18.48 | 325.27 | -31.08 | 1.78 | 1.55 |
| Entry 429 Wellesley Street | 0.74 | 48.75 | -27.37 | 0.77 | 0.40 |
| Pakuranga Road | 6.18 | 355.35 | -24.14 | 3.78 | 3.51 |
| Great South Road | 9.32 | 280.80 | -21.78 | 6.19 | 5.70 |
| Great North Road | 12.42 | 422.70 | -20.43 | 8.16 | 7.59 |
| East Coast Road | 4.95 | 73.57 | -20.36 | 2.57 | 1.70 |

### NZ6_s2, H-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Northern Motorway | 25.69 | 4499.07 | -150.72 | 20.16 | 20.16 |
| Southern Motorway | 41.89 | 5634.41 | -145.94 | 27.38 | 27.33 |
| Northwestern Motorway | 25.14 | 3542.93 | -130.92 | 16.44 | 16.28 |
| Tamaki Drive | 7.86 | 230.45 | -58.12 | 7.18 | 5.78 |
| Southwestern Motorway | 14.52 | 350.42 | -56.83 | 2.00 | 1.58 |
| Dominion Road | 6.14 | 187.34 | -35.21 | 4.73 | 3.99 |
| Upper Harbour Motorway | 14.44 | 1010.29 | -34.45 | 10.35 | 9.99 |
| Onewa Road | 2.30 | 106.83 | -33.49 | 2.05 | 1.45 |
| Kepa Road | 2.31 | 87.66 | -31.96 | 1.92 | 1.27 |
| Entry 424 Fanshawe Street | 0.61 | 46.95 | -31.37 | 0.60 | 0.24 |
| Mount Eden Road | 4.94 | 101.27 | -27.90 | 3.68 | 2.76 |
| Great North Road | 11.81 | 412.74 | -26.07 | 7.91 | 7.37 |

### NZ6_s2, R-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Northern Motorway | 25.69 | 4503.40 | -112.66 | 20.16 | 20.16 |
| Northwestern Motorway | 25.14 | 3547.76 | -110.93 | 16.47 | 16.34 |
| Southwestern Motorway | 14.52 | 356.95 | -68.97 | 2.05 | 1.53 |
| Tamaki Drive | 7.86 | 226.29 | -42.40 | 7.09 | 6.01 |
| Dominion Road | 6.14 | 183.44 | -37.44 | 4.65 | 3.72 |
| Onewa Road | 2.30 | 109.28 | -35.12 | 2.09 | 1.46 |
| Great North Road | 11.81 | 414.05 | -34.56 | 7.96 | 7.10 |
| Te Atatu Road | 5.59 | 200.69 | -33.58 | 3.76 | 3.21 |
| Southern Motorway | 41.89 | 5665.10 | -32.63 | 27.37 | 27.68 |
| Entry 424 Fanshawe Street | 0.61 | 48.60 | -32.09 | 0.61 | 0.24 |
| Edmonton Road | 2.94 | 106.55 | -30.00 | 2.19 | 1.61 |
| Upper Harbour Motorway | 14.44 | 1010.29 | -28.46 | 10.35 | 10.06 |

### NZ6_s3, H-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Northwestern Motorway | 25.14 | 3558.90 | -162.30 | 16.46 | 16.22 |
| Northern Motorway | 25.38 | 4403.40 | -152.20 | 19.87 | 19.87 |
| Southern Motorway | 41.89 | 5703.72 | -144.66 | 27.37 | 27.28 |
| Tamaki Drive | 9.74 | 336.98 | -107.09 | 10.38 | 7.58 |
| Southwestern Motorway | 17.10 | 411.43 | -58.90 | 2.40 | 1.97 |
| Great North Road | 10.54 | 418.38 | -51.12 | 7.81 | 6.92 |
| Dominion Road | 6.29 | 210.08 | -42.20 | 4.86 | 4.07 |
| Mount Eden Road | 5.02 | 128.24 | -41.82 | 4.49 | 3.22 |
| Entry 429 Wellesley Street | 0.74 | 45.63 | -38.05 | 0.79 | 0.16 |
| Lake Road | 5.92 | 172.17 | -33.38 | 4.19 | 3.53 |
| Pakuranga Road | 5.77 | 330.71 | -30.41 | 3.55 | 3.20 |
| Onewa Road | 2.30 | 98.03 | -23.72 | 1.93 | 1.50 |

### NZ6_s3, R-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Southern Motorway | 41.89 | 5714.38 | -190.20 | 27.39 | 27.47 |
| Northwestern Motorway | 25.14 | 3565.81 | -107.18 | 16.48 | 16.27 |
| Northern Motorway | 25.38 | 4405.22 | -103.31 | 19.87 | 19.87 |
| Tamaki Drive | 9.74 | 352.49 | -95.87 | 10.87 | 8.21 |
| Southwestern Motorway | 17.10 | 410.88 | -88.21 | 2.40 | 1.74 |
| Great North Road | 10.54 | 422.95 | -80.76 | 7.83 | 6.21 |
| Dominion Road | 6.29 | 207.17 | -39.41 | 4.79 | 4.02 |
| Entry 429 Wellesley Street | 0.74 | 50.49 | -38.16 | 0.86 | 0.24 |
| Lake Road | 5.92 | 170.47 | -31.23 | 4.16 | 3.57 |
| Atkinson Road | 2.19 | 97.13 | -29.16 | 3.68 | 2.61 |
| Titirangi Road | 2.99 | 89.38 | -28.39 | 2.39 | 1.68 |
| Manukau Road | 4.16 | 121.42 | -26.10 | 3.31 | 2.66 |

### NZ18_s1, H-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Southern Motorway | 41.89 | 5582.37 | -279.34 | 27.38 | 27.27 |
| Northern Motorway | 25.38 | 4382.33 | -251.95 | 19.87 | 19.87 |
| Northwestern Motorway | 25.14 | 3500.31 | -241.21 | 16.59 | 16.11 |
| Dominion Road | 6.14 | 243.95 | -113.89 | 5.77 | 3.42 |
| Mount Eden Road | 4.95 | 145.94 | -79.53 | 5.09 | 2.52 |
| Southwestern Motorway | 18.48 | 322.89 | -70.59 | 1.77 | 1.25 |
| Tamaki Drive | 9.74 | 267.19 | -68.41 | 8.51 | 6.72 |
| Manukau Road | 4.14 | 132.07 | -60.11 | 3.52 | 2.10 |
| Great North Road | 12.42 | 423.67 | -54.69 | 8.19 | 6.86 |
| Pakuranga Road | 6.18 | 355.35 | -48.29 | 3.78 | 3.31 |
| Entry 429 Wellesley Street | 0.74 | 48.77 | -45.21 | 0.77 | 0.10 |
| Sandringham Road | 3.40 | 101.58 | -33.26 | 3.00 | 2.17 |

### NZ18_s1, R-clock

| street | km | veh_h_before | veh_h_change | delay_per_car_0709_before | delay_per_car_0709_charge |
|---|---|---|---|---|---|
| Southern Motorway | 41.89 | 5587.56 | -263.28 | 27.39 | 27.27 |
| Northern Motorway | 25.38 | 4384.18 | -253.64 | 19.87 | 19.87 |
| Northwestern Motorway | 25.14 | 3506.31 | -233.42 | 16.59 | 16.14 |
| Dominion Road | 6.14 | 241.27 | -107.35 | 5.71 | 3.46 |
| Southwestern Motorway | 18.48 | 325.27 | -76.02 | 1.78 | 1.23 |
| Mount Eden Road | 4.95 | 145.56 | -73.90 | 5.08 | 2.65 |
| Tamaki Drive | 9.74 | 269.11 | -70.08 | 8.55 | 6.76 |
| Manukau Road | 4.14 | 132.61 | -62.77 | 3.54 | 2.04 |
| Pakuranga Road | 6.18 | 355.35 | -53.19 | 3.78 | 3.23 |
| Great North Road | 12.42 | 422.70 | -49.32 | 8.16 | 6.97 |
| Entry 429 Wellesley Street | 0.74 | 48.75 | -43.14 | 0.77 | 0.14 |
| Kepa Road | 2.38 | 65.85 | -34.79 | 1.53 | 0.75 |

## street-hours where delay grew by more than 1 vehicle-hour

| scenario | arm | street | bin | veh_h_before | veh_h_change |
|---|---|---|---|---|---|
| NZ6_s1 | H-clock | Titirangi Road | 07:00-08:00 | 22.2 | 2.0 |
| NZ6_s1 | H-clock | Great North Road | 07:00-08:00 | 101.6 | 1.7 |
| NZ6_s1 | H-clock | Lake Road | 07:00-08:00 | 24.3 | 1.5 |
| NZ6_s1 | H-clock | Upper Harbour Motorway | 07:00-08:00 | 341.3 | 1.2 |
| NZ6_s1 | H-clock | 20 | 07:00-08:00 | 3.7 | 1.1 |
| NZ6_s1 | R-clock | Southern Motorway | 06:00-07:00 | 287.0 | 150.9 |
| NZ6_s1 | R-clock | Southern Motorway | 07:00-08:00 | 1700.3 | 35.0 |
| NZ6_s1 | R-clock | Northern Motorway | 06:00-07:00 | 646.1 | 21.8 |
| NZ6_s1 | R-clock | Dominion Road | 07:00-08:00 | 51.4 | 13.3 |
| NZ6_s1 | R-clock | Northwestern Motorway | 06:00-07:00 | 273.2 | 9.3 |
| NZ6_s1 | R-clock | Kepa Road | 07:00-08:00 | 14.5 | 5.8 |
| NZ6_s1 | R-clock | Entry 429 Wellesley Street | 07:00-08:00 | 11.1 | 5.7 |
| NZ6_s1 | R-clock | Ngapipi Road | 07:00-08:00 | 3.9 | 5.2 |
| NZ6_s1 | R-clock | Stanley Street | 07:00-08:00 | 11.8 | 3.8 |
| NZ6_s1 | R-clock | Ian McKinnon Drive | 07:00-08:00 | 5.2 | 3.5 |
| NZ6_s1 | R-clock | Sandringham Road | 07:00-08:00 | 27.8 | 3.1 |
| NZ6_s1 | R-clock | West Tamaki Road | 07:00-08:00 | 14.9 | 3.1 |
| NZ6_s1 | R-clock | Upper Harbour Motorway | 07:00-08:00 | 342.2 | 3.0 |
| NZ6_s1 | R-clock | Tamaki Drive | 07:00-08:00 | 68.4 | 2.9 |
| NZ6_s1 | R-clock | Exit 2 Southern Motorway | 07:00-08:00 | 3.6 | 2.8 |
| NZ6_s1 | R-clock | East Coast Road | 06:00-07:00 | 3.2 | 2.6 |
| NZ6_s1 | R-clock | Saint Heliers Bay Road | 07:00-08:00 | 11.1 | 2.5 |
| NZ6_s1 | R-clock | Dominion Road | 06:00-07:00 | 2.3 | 2.3 |
| NZ6_s1 | R-clock | Portage Road | 07:00-08:00 | 12.7 | 2.0 |
| NZ6_s1 | R-clock | Kohimarama Road | 07:00-08:00 | 8.9 | 2.0 |
| NZ6_s1 | R-clock | Saint Leonards Road | 07:00-08:00 | 7.1 | 1.9 |
| NZ6_s1 | R-clock | Golf Road | 07:00-08:00 | 22.5 | 1.9 |
| NZ6_s1 | R-clock | New North Road | 07:00-08:00 | 25.9 | 1.8 |
| NZ6_s1 | R-clock | Mount Eden Road | 06:00-07:00 | 1.2 | 1.8 |
| NZ6_s1 | R-clock | Saint Jude Street | 07:00-08:00 | 1.7 | 1.4 |
| NZ6_s1 | R-clock | Manukau Road | 06:00-07:00 | 0.9 | 1.4 |
| NZ6_s1 | R-clock | The Strand | 07:00-08:00 | 2.4 | 1.3 |
| NZ6_s1 | R-clock | 20 | 07:00-08:00 | 3.7 | 1.2 |
| NZ6_s1 | R-clock | Carrington Road | 07:00-08:00 | 7.6 | 1.1 |
| NZ6_s1 | R-clock | Great North Road | 07:00-08:00 | 101.7 | 1.1 |
| NZ6_s2 | H-clock | Portage Road | 07:00-08:00 | 10.3 | 2.2 |
| NZ6_s2 | H-clock | Surrey Crescent | 07:00-08:00 | 5.5 | 1.5 |
| NZ6_s2 | H-clock | Golf Road | 07:00-08:00 | 17.6 | 1.2 |
| NZ6_s2 | H-clock | College Hill | 07:00-08:00 | 6.7 | 1.0 |
| NZ6_s2 | R-clock | Southern Motorway | 07:00-08:00 | 1699.0 | 56.6 |
| NZ6_s2 | R-clock | Northwestern Motorway | 06:00-07:00 | 261.1 | 40.7 |
| NZ6_s2 | R-clock | Southern Motorway | 06:00-07:00 | 396.0 | 14.2 |
| NZ6_s2 | R-clock | Northern Motorway | 06:00-07:00 | 673.5 | 5.7 |
| NZ6_s2 | R-clock | Dominion Road | 07:00-08:00 | 30.5 | 2.7 |
| NZ6_s2 | R-clock | Entry 429 Wellesley Street | 07:00-08:00 | 5.3 | 2.3 |
| NZ6_s2 | R-clock | Chivalry Road | 07:00-08:00 | 5.7 | 2.1 |
| NZ6_s2 | R-clock | Atkinson Road | 06:00-07:00 | 1.7 | 1.7 |
| NZ6_s2 | R-clock | Surrey Crescent | 07:00-08:00 | 5.5 | 1.6 |
| NZ6_s2 | R-clock | Great North Road | 06:00-07:00 | 5.1 | 1.6 |
| NZ6_s2 | R-clock | Stanley Street | 07:00-08:00 | 6.1 | 1.6 |
| NZ6_s2 | R-clock | Great South Road | 07:00-08:00 | 66.2 | 1.5 |
| NZ6_s2 | R-clock | Abbotts Way | 08:00-09:00 | 35.8 | 1.2 |
| NZ6_s2 | R-clock | Ponsonby Road | 08:00-09:00 | 20.3 | 1.1 |
| NZ6_s2 | R-clock | Manukau Road | 07:00-08:00 | 18.6 | 1.1 |
| NZ6_s2 | R-clock | Tamaki Drive | 07:00-08:00 | 55.4 | 1.1 |
| NZ6_s2 | R-clock | Nugent Street | 07:00-08:00 | 3.2 | 1.1 |
| NZ6_s3 | H-clock | Great North Road | 07:00-08:00 | 104.3 | 9.5 |
| NZ6_s3 | H-clock | Southwestern Motorway | 07:00-08:00 | 98.5 | 7.5 |
| NZ6_s3 | H-clock | Titirangi Road | 07:00-08:00 | 25.8 | 7.1 |
| NZ6_s3 | H-clock | Saint Jude Street | 07:00-08:00 | 5.4 | 3.1 |
| NZ6_s3 | H-clock | Atkinson Road | 07:00-08:00 | 32.1 | 3.0 |
| NZ6_s3 | H-clock | 20 | 07:00-08:00 | 6.8 | 2.7 |
| NZ6_s3 | H-clock | Ngapipi Road | 07:00-08:00 | 8.5 | 2.3 |
| NZ6_s3 | H-clock | New North Road | 07:00-08:00 | 21.9 | 2.3 |
| NZ6_s3 | H-clock | Kepa Road | 07:00-08:00 | 21.9 | 1.7 |
| NZ6_s3 | H-clock | Pakuranga Road | 07:00-08:00 | 74.8 | 1.0 |
| NZ6_s3 | R-clock | Northwestern Motorway | 06:00-07:00 | 279.4 | 39.8 |
| NZ6_s3 | R-clock | Southern Motorway | 07:00-08:00 | 1713.6 | 21.0 |
| NZ6_s3 | R-clock | Northwestern Motorway | 07:00-08:00 | 1144.0 | 13.0 |
| NZ6_s3 | R-clock | Dominion Road | 07:00-08:00 | 45.1 | 9.1 |
| NZ6_s3 | R-clock | Mount Eden Road | 07:00-08:00 | 32.1 | 6.1 |
| NZ6_s3 | R-clock | Manukau Road | 07:00-08:00 | 27.0 | 4.0 |
| NZ6_s3 | R-clock | Great North Road | 06:00-07:00 | 7.3 | 3.4 |
| NZ6_s3 | R-clock | Ian McKinnon Drive | 07:00-08:00 | 3.4 | 2.6 |
| NZ6_s3 | R-clock | Sandringham Road | 07:00-08:00 | 13.3 | 2.5 |
| NZ6_s3 | R-clock | Swanson Road | 07:00-08:00 | 27.5 | 2.2 |
| NZ6_s3 | R-clock | Green Lane E | 07:00-08:00 | 12.6 | 2.1 |
| NZ6_s3 | R-clock | Entry 429 Wellesley Street | 07:00-08:00 | 2.4 | 1.9 |
| NZ6_s3 | R-clock | Remuera Road | 07:00-08:00 | 23.2 | 1.9 |
| NZ6_s3 | R-clock | Ladies Mile | 07:00-08:00 | 5.4 | 1.7 |
| NZ6_s3 | R-clock | Nugent Street | 07:00-08:00 | 2.0 | 1.6 |
| NZ6_s3 | R-clock | Titirangi Road | 06:00-07:00 | 1.0 | 1.6 |
| NZ6_s3 | R-clock | Stanley Street | 07:00-08:00 | 4.8 | 1.5 |
| NZ6_s3 | R-clock | Blockhouse Bay Road | 07:00-08:00 | 15.1 | 1.4 |
| NZ6_s3 | R-clock | Dairy Flat Highway | 06:00-07:00 | 2.1 | 1.4 |
| NZ6_s3 | R-clock | Alpers Avenue | 07:00-08:00 | 1.3 | 1.3 |
| NZ6_s3 | R-clock | Abbotts Way | 07:00-08:00 | 7.4 | 1.3 |
| NZ6_s3 | R-clock | Exit 4A Northern Motorway | 07:00-08:00 | 0.6 | 1.2 |
| NZ6_s3 | R-clock | Exit 429B Wellesley Street | 07:00-08:00 | 3.5 | 1.2 |
| NZ6_s3 | R-clock | Onehunga Mall | 08:00-09:00 | 13.9 | 1.1 |
| NZ6_s3 | R-clock | Dominion Road | 06:00-07:00 | 2.0 | 1.1 |

