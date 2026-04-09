"""Unit tests for great circle distance UDFs.

Tests call the underlying bare Python functions directly, which lets
you run them locally without a Flink environment.
"""

import pandas as pd
import pytest

from great_circle_distance.distance import _f_great_circle_km, _f_great_circle_km_vec


# ---------------------------------------------------------------------------
# Scalar variant
# ---------------------------------------------------------------------------


def test_same_point_is_zero() -> None:
    assert _f_great_circle_km(0.0, 0.0, 0.0, 0.0) == pytest.approx(0.0)


def test_paris_to_london() -> None:
    # Paris: 48.8566°N, 2.3522°E  |  London: 51.5074°N, 0.1278°W
    distance_km = _f_great_circle_km(48.8566, 2.3522, 51.5074, -0.1278)
    assert distance_km == pytest.approx(343.5, rel=0.01)


def test_new_york_to_london() -> None:
    # New York: 40.7128°N, 74.0060°W  |  London: 51.5074°N, 0.1278°W
    distance_km = _f_great_circle_km(40.7128, -74.0060, 51.5074, -0.1278)
    assert distance_km == pytest.approx(5570.0, rel=0.01)


def test_symmetry() -> None:
    a_to_b = _f_great_circle_km(48.8566, 2.3522, 51.5074, -0.1278)
    b_to_a = _f_great_circle_km(51.5074, -0.1278, 48.8566, 2.3522)
    assert a_to_b == pytest.approx(b_to_a)


def test_antipodal_points() -> None:
    # Antipodal: maximum possible great circle distance ≈ πR ≈ 20015 km
    distance_km = _f_great_circle_km(0.0, 0.0, 0.0, 180.0)
    assert distance_km == pytest.approx(20015.0, rel=0.01)


# ---------------------------------------------------------------------------
# Vectorized variant
# ---------------------------------------------------------------------------


def test_vec_same_point_is_zero() -> None:
    result = _f_great_circle_km_vec(
        pd.Series([0.0]), pd.Series([0.0]), pd.Series([0.0]), pd.Series([0.0])
    )
    assert list(result) == pytest.approx([0.0])


def test_vec_matches_scalar_for_single_row() -> None:
    scalar = _f_great_circle_km(48.8566, 2.3522, 51.5074, -0.1278)
    result = _f_great_circle_km_vec(
        pd.Series([48.8566]),
        pd.Series([2.3522]),
        pd.Series([51.5074]),
        pd.Series([-0.1278]),
    )
    assert list(result) == pytest.approx([scalar])


def test_vec_batch_multiple_rows() -> None:
    # Compute two distances in a single batch
    result = _f_great_circle_km_vec(
        pd.Series([48.8566, 40.7128]),
        pd.Series([2.3522, -74.0060]),
        pd.Series([51.5074, 51.5074]),
        pd.Series([-0.1278, -0.1278]),
    )
    assert result[0] == pytest.approx(343.5, rel=0.01)
    assert result[1] == pytest.approx(5570.0, rel=0.01)
