# You can write tests which exercise the underlying Python functions
# of each UDF to determine if they are functional.

from example_udf.scalar import _f_int_add, _f_str_concat


def test_int_add() -> None:
    found = _f_int_add(1, 2)
    assert found == 3


def test_str_concat() -> None:
    found = _f_str_concat("hi", "bye")
    assert found == "hibye"
