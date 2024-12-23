import threading
from unittest.mock import Mock, patch

import pytest

from src.core.timer.timer import Timer


@pytest.fixture
def timer_instance() -> Timer:
    return Timer()


def test_start_sets_interval_and_function(timer_instance: Timer) -> None:
    # Given
    interval = 5
    function = Mock()

    # When
    with patch.object(timer_instance, "_reset_timer") as mock_reset_timer:
        timer_instance.start(interval, function)

    # Then
    assert timer_instance.interval == interval
    assert timer_instance.function == function
    assert not timer_instance._cancelled
    mock_reset_timer.assert_called_once()


def test_start_with_zero_interval_raises_value_error(timer_instance: Timer) -> None:
    # Given
    interval = 0
    function = Mock()

    # When / Then
    with pytest.raises(ValueError, match="Interval must be greater than 0"):
        timer_instance.start(interval, function)


def test_reset_timer_starts_new_timer(timer_instance: Timer) -> None:
    # Given
    timer_instance.interval = 5
    timer_instance._cancelled = False

    # When
    with patch("threading.Timer") as mock_timer:
        timer_instance._reset_timer()

    # Then
    mock_timer.assert_called_once_with(5, timer_instance._execute)
    mock_timer.return_value.start.assert_called_once()


def test_execute_calls_function_and_resets_timer(timer_instance: Timer) -> None:
    # Given
    function = Mock()
    timer_instance.function = function
    timer_instance._cancelled = False

    # When
    with patch.object(timer_instance, "_reset_timer") as mock_reset_timer:
        timer_instance._execute()

    # Then
    function.assert_called_once()
    mock_reset_timer.assert_called_once()


def test_cancel_stops_timer(timer_instance: Timer) -> None:
    # Given
    mock_timer = Mock(threading.Timer)
    timer_instance._timer = mock_timer

    # When
    timer_instance.cancel()

    # Then
    assert timer_instance._cancelled
    mock_timer.cancel.assert_called_once()
    assert timer_instance._timer is None


def test_cancel_when_no_timer(timer_instance: Timer) -> None:
    # Given
    timer_instance._timer = None

    # When
    timer_instance.cancel()

    # Then
    assert timer_instance._cancelled
    assert timer_instance._timer is None


def test_reset_timer_cancels_existing_timer(timer_instance: Timer) -> None:
    # Given
    timer_instance.interval = 5
    timer_instance._cancelled = False
    mock_timer = Mock(threading.Timer)
    timer_instance._timer = mock_timer

    # When
    with patch("threading.Timer") as mock_new_timer:
        timer_instance._reset_timer()

    # Then
    mock_timer.cancel.assert_called_once()
    mock_new_timer.assert_called_once_with(5, timer_instance._execute)
    mock_new_timer.return_value.start.assert_called_once()
