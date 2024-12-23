import multiprocessing
from typing import Generator
from unittest.mock import Mock, patch

import pytest

from data.workers.whisper_worker import WhisperConfig, WhisperWorker


@pytest.fixture
def whisper_config() -> WhisperConfig:
    return WhisperConfig(device="cuda", model_name="tiny", model_download_path="/tmp")


@pytest.fixture
def whisper_worker() -> Generator[WhisperWorker, None, None]:
    worker = WhisperWorker()
    yield worker
    worker.stop()


def test_transcribe_sends_correct_command(whisper_worker: WhisperWorker, whisper_config: WhisperConfig) -> None:
    with patch("multiprocessing.Process") as MockProcess, patch(
        "data.workers.whisper_worker.whisper.load_model"
    ) as mock_load_model:
        mock_process = Mock()
        MockProcess.return_value = mock_process
        mock_model = Mock()
        mock_load_model.return_value = mock_model

        # Given
        whisper_worker.start(whisper_config)
        file_path = "test.wav"
        language = "en"

        # When
        with patch.object(whisper_worker._pipe_parent, "send") as mock_send, patch.object(
            whisper_worker._pipe_parent, "recv", return_value={}
        ):
            whisper_worker.transcribe(file_path, language)

            # Then
            mock_send.assert_called_once_with(("transcribe", (file_path, language)))


def test_transcribe_raises_error_if_worker_not_running(whisper_worker: WhisperWorker) -> None:
    # Given
    file_path = "test.wav"
    language = "en"

    # When / Then
    with pytest.raises(RuntimeError, match="Worker process is not running"):
        whisper_worker.transcribe(file_path, language)


def test_initialize_shared_object(whisper_config: WhisperConfig) -> None:
    worker = WhisperWorker()
    with patch("data.workers.whisper_worker.whisper.load_model") as mock_load_model:
        mock_model = Mock()
        mock_load_model.return_value = mock_model
        mock_model.to.return_value = mock_model

        # When
        model = worker.initialize_shared_object(whisper_config)

        # Then
        mock_load_model.assert_called_once_with(
            whisper_config.model_name,
            download_root=whisper_config.model_download_path,
        )
        assert model == mock_model


def test_handle_command_transcribe(whisper_config: WhisperConfig) -> None:
    worker = WhisperWorker()
    model = Mock()
    pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()

    file_path = "test.wav"
    language = "en"
    command = "transcribe"
    args = (file_path, language)

    with patch.object(model, "transcribe", return_value={"text": "transcribed text"}):
        # When
        worker.handle_command(command, args, model, whisper_config, pipe, is_processing, processing_lock)

        # Then
        model.transcribe.assert_called_once_with(file_path, language="en")
        pipe.send.assert_called_once_with({"text": "transcribed text"})


def test_handle_command_transcribe_error(whisper_config: WhisperConfig) -> None:
    worker = WhisperWorker()
    model = Mock()
    pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()

    file_path = "test.wav"
    language = "en"
    command = "transcribe"
    args = (file_path, language)

    with patch.object(model, "transcribe", side_effect=RuntimeError("Transcription error")):
        # When
        worker.handle_command(command, args, model, whisper_config, pipe, is_processing, processing_lock)

        # Then
        assert pipe.send.call_count == 1
        sent_exception = pipe.send.call_args[0][0]
        assert isinstance(sent_exception, RuntimeError)
        assert str(sent_exception) == "Transcription error"
