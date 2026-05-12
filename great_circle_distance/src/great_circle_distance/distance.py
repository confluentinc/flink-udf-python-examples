"""Great circle distance UDFs using the haversine formula.

Two variants are provided:

- ``great_circle_km``: scalar UDF. Processes one row at a time using
  Python's ``math`` module. Simple and dependency-free; use for low- to
  moderate-throughput pipelines.

- ``great_circle_km_vec``: vectorized UDF (``func_type="pandas"``).
  Flink batches rows into ``pandas.Series`` objects, which are then
  processed with NumPy element-wise operations. This avoids per-row
  Python overhead and achieves ~50–100× higher throughput than the
  scalar variant for large batches.

Both functions return the distance in **kilometres** and accept
coordinates as decimal degrees (latitude −90 … +90, longitude −180 …
+180).

The underlying bare Python functions (``_f_great_circle_km`` and
``_f_great_circle_km_vec``) are exported so they can be unit-tested
locally without a Flink runtime.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd
from pyflink.table import DataTypes
from pyflink.table.types import DataType
from pyflink.table.udf import udf

_EARTH_RADIUS_KM: float = 6371.0


# ---------------------------------------------------------------------------
# Scalar variant — row-by-row, pure Python, no extra deps beyond apache-flink
# ---------------------------------------------------------------------------


def _f_great_circle_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    """Haversine formula for great circle distance in kilometres.

    Args:
        lat1: Latitude of point A in decimal degrees.
        lon1: Longitude of point A in decimal degrees.
        lat2: Latitude of point B in decimal degrees.
        lon2: Longitude of point B in decimal degrees.

    Returns:
        Great circle distance between A and B in kilometres.
    """
    lat1_r = math.radians(lat1)
    lat2_r = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon / 2) ** 2
    )
    # Clamp to [0, 1] to guard against floating-point values slightly outside
    # the valid domain of asin, which would raise ValueError.
    a = min(1.0, max(0.0, a))
    return _EARTH_RADIUS_KM * 2 * math.asin(math.sqrt(a))


_great_circle_km_input_types: list[DataType] = [
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
]
great_circle_km = udf(
    _f_great_circle_km,
    input_types=_great_circle_km_input_types,
    result_type=DataTypes.DOUBLE(),
)


# ---------------------------------------------------------------------------
# Vectorized variant — pandas Series in/out, NumPy batch ops
# ---------------------------------------------------------------------------


def _f_great_circle_km_vec(
    lat1: pd.Series[Any],
    lon1: pd.Series[Any],
    lat2: pd.Series[Any],
    lon2: pd.Series[Any],
) -> pd.Series[Any]:
    """Vectorized haversine formula using NumPy — ~50–100× faster than the
    scalar variant when Flink batches are large.

    Flink passes each argument as a ``pandas.Series`` of floats.  NumPy
    element-wise operations (``np.sin``, ``np.cos``, ``np.arcsin``) run
    in compiled C loops over the whole batch, avoiding per-row Python
    interpreter overhead.

    Args:
        lat1: Latitudes of point A (decimal degrees).
        lon1: Longitudes of point A (decimal degrees).
        lat2: Latitudes of point B (decimal degrees).
        lon2: Longitudes of point B (decimal degrees).

    Returns:
        Great circle distances in kilometres as a ``pandas.Series``.
    """
    lat1_r = np.radians(lat1)
    lat2_r = np.radians(lat2)
    dlat = np.radians(lat2 - lat1)
    dlon = np.radians(lon2 - lon1)
    a = np.sin(dlat / 2) ** 2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon / 2) ** 2
    # Clamp to [0, 1] to guard against floating-point values slightly outside
    # the valid domain of arcsin, which would produce NaN.
    a = np.clip(a, 0.0, 1.0)
    return pd.Series(_EARTH_RADIUS_KM * 2 * np.arcsin(np.sqrt(a)))


_great_circle_km_vec_input_types: list[DataType] = [
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
    DataTypes.DOUBLE(),
]


@udf(  # type: ignore[untyped-decorator]
    input_types=_great_circle_km_vec_input_types,
    result_type=DataTypes.DOUBLE(),
    func_type="pandas",
)
def great_circle_km_vec(
    lat1: pd.Series[Any],
    lon1: pd.Series[Any],
    lat2: pd.Series[Any],
    lon2: pd.Series[Any],
) -> pd.Series[Any]:
    return _f_great_circle_km_vec(lat1, lon1, lat2, lon2)
