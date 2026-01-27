from pyflink.table.udf import FunctionContext

from pii_mask import MaskPii


MOCK_CTX = FunctionContext({}, {})  # type: ignore[no-untyped-call]


def test_mask_pii() -> None:
    f = MaskPii()
    f.open(MOCK_CTX)

    found = f.eval("How are you John Doe?")

    expected = "How are you ****?"
    assert found == expected
