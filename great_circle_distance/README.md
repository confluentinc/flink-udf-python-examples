# Great Circle Distance UDF

This example demonstrates two Python UDFs that compute the **great circle
distance** (shortest path over a sphere) between two geographic coordinates.

> **Great circle distance** is the angular distance between two points on a
> sphere, converted to a surface distance using Earth's mean radius
> (6371 km). The [haversine formula](https://en.wikipedia.org/wiki/Haversine_formula)
> is used here, which is numerically stable for all distances.

## Files

- `src/great_circle_distance/distance.py` — both UDF implementations
- `pyproject.toml` — project configuration and dependencies
- `flink_sql_complete.sql` — complete SQL to register and test the UDFs

## UDF Variants

### `great_circle_km` — scalar

Processes one row at a time using Python's `math` module. No extra
dependencies. Use this for simple pipelines where throughput is not a
concern.

```sql
SELECT great_circle_km(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon) AS distance_km
FROM ride_events;
```

### `great_circle_km_vec` — vectorized (recommended for high throughput)

Uses `func_type="pandas"`: Flink batches multiple rows into
`pandas.Series` objects and passes them to the function at once.
NumPy's C-compiled element-wise operations (`np.sin`, `np.cos`,
`np.arcsin`) then run over the whole batch in a single call, avoiding
per-row Python interpreter overhead. Expect **~50–100× higher
throughput** over the scalar variant when batch sizes are large.

```sql
SELECT great_circle_km_vec(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon) AS distance_km
FROM ride_events;
```

Both functions return the distance in **kilometres** and accept
coordinates as decimal degrees.

## Performance Notes

| Approach | Per-row overhead | When to use |
|---|---|---|
| `great_circle_km` (scalar, `math`) | ~1 µs / row | Low volume, simplicity |
| `great_circle_km_vec` (vectorized, NumPy) | ~10–20 ns / row (amortised) | High-throughput pipelines |

### Other Libraries

If you need **ellipsoidal accuracy** (WGS-84, not a sphere), consider:

- [`geopy.distance.geodesic()`](https://geopy.readthedocs.io/en/stable/#geopy.distance.geodesic) —
  Vincenty's formulae; ~0.5 mm accuracy; row-by-row only.
- [`pyproj.Geod.inv()`](https://pyproj4.github.io/pyproj/stable/api/geod.html) —
  PROJ C library; accepts NumPy arrays for bulk computation; most accurate.

For the haversine formula the error vs. the true geodesic is typically
< 0.3%, which is sufficient for most applications.

## Usage

1. **Build and upload** — follow the instructions in the
   [project-level README](../README.md).

2. **Run the SQL** — execute the statements in `flink_sql_complete.sql`
   in order, replacing `<artifact-id>` with the ID returned by
   `confluent flink artifact create`.
