import numpy as np
import pytest

from ds_toolbox import baselines as bl


def test_naive_mean_and_drift():
    h = [1.0, 2.0, 3.0, 4.0]
    assert list(bl.naive(h, 2)) == [4.0, 4.0]
    assert list(bl.mean(h, 1)) == [2.5]
    assert np.allclose(bl.drift(h, 3), [5.0, 6.0, 7.0])
    assert list(bl.drift([7.0], 2)) == [7.0, 7.0]


def test_seasonal_naive_repeats_the_last_season():
    f = bl.seasonal_naive(3)
    assert f.__name__ == "seasonal_naive_3"
    assert list(f([0, 0, 1, 2, 3], 5)) == [1, 2, 3, 1, 2]
    with pytest.raises(ValueError, match="shorter"):
        f([1, 2], 1)
    with pytest.raises(ValueError):
        bl.seasonal_naive(0)


def test_empty_history_is_refused():
    with pytest.raises(ValueError, match="empty"):
        bl.naive([], 1)


def test_majority_class():
    assert bl.majority_class(["a", "b", "b", None]) == "b"
    with pytest.raises(ValueError):
        bl.majority_class([None])
