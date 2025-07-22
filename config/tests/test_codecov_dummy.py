import pytest

from dev_env.codecov_dummy import covered_function, uncovered_function


def test_covered_function():
    assert covered_function() == 1


@pytest.mark.skip(reason="This is a dummy test")
def test_uncovered_function():
    assert uncovered_function() == 2
