import pytest

from easyprocess import EasyProcess

# if run with coverage:
#        Fatal Python error: deallocating None


@pytest.mark.timeout(1000)
def test_timeout():  # pragma: no cover
    for x in range(1000):
        print("index=", x)
        assert EasyProcess("sleep 5").call(timeout=0.05).return_code != 0
