import multiprocessing
from multiprocessing.sharedctypes import Synchronized
from typing import Generator
from unittest.mock import Mock, patch

import pytest

from core.logger.logger import Logger
from data.workers.base_worker import BaseWorker


class MockBaseWorker(BaseWorker[str, str, dict, None]):  # type: ignore
    def _run_process(
        self,
        config: str,
        pipe: multiprocessing.connection.Connection,
        stop_event: multiprocessing.synchronize.Event,
        is_processing: multiprocessing.Value,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        pass

    def initialize_shared_object(
        self,
        config: str,
    ) -> None:
        return None

    def handle_command(
        self,
        command: str,
        args: str,
        shared_object: None,
        config: str,
        pipe: multiprocessing.connection.Connection,
        is_processing: Synchronized,  # type: ignore
        processing_lock: multiprocessing.synchronize.Lock,
    ) -> None:
        pass

    def get_worker_name(self) -> str:
        return "MockBaseWorker"


@pytest.fixture
def base_worker(base_config: str, mock_logger: Logger) -> Generator[MockBaseWorker, None, None]:
    worker = MockBaseWorker(base_config, mock_logger)
    yield worker
    worker.stop()


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def base_config() -> str:
    return "cpu"


def test_start_creates_new_process(base_worker: MockBaseWorker) -> None:
    # Given
    with patch("multiprocessing.Process") as MockProcess:
        mock_process = Mock()
        MockProcess.return_value = mock_process

        # When
        base_worker.start()

        # Then
        MockProcess.assert_called_once()
        mock_process.start.assert_called_once()
        assert base_worker.is_alive()
        assert not base_worker.is_processing()


def test_stop_terminates_process(base_worker: MockBaseWorker) -> None:
    with patch("multiprocessing.Process") as MockProcess:
        mock_process = Mock()
        MockProcess.return_value = mock_process

        # Given
        base_worker.start()
        assert base_worker.is_alive()

        # When
        base_worker.stop()

        # Then
        mock_process.join.assert_called_once_with(timeout=5)
        mock_process.terminate.assert_called_once()
        assert not base_worker.is_alive()


def test_is_alive_returns_correct_status(base_worker: MockBaseWorker) -> None:
    with patch("multiprocessing.Process") as MockProcess:
        mock_process = Mock()
        MockProcess.return_value = mock_process

        # Given
        base_worker.start()

        # When
        alive_status = base_worker.is_alive()

        # Then
        assert alive_status

        # When
        base_worker.stop()
        alive_status = base_worker.is_alive()

        # Then
        assert not alive_status


def test_is_processing_returns_correct_status(base_worker: MockBaseWorker) -> None:
    # Given
    base_worker._is_processing.value = True

    # When
    processing_status = base_worker.is_processing()

    # Then
    assert processing_status

    # Given
    base_worker._is_processing.value = False

    # When
    processing_status = base_worker.is_processing()

    # Then
    assert not processing_status
