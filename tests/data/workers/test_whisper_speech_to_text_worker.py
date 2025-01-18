import multiprocessing
from typing import Any, Generator
from unittest.mock import Mock, patch

import pytest

from core.logger.logger import Logger
from data.workers.whisper_speech_to_text_worker import (
    WhisperSpeechToTextConfig,
    WhisperSpeechToTextWorker,
)


@pytest.fixture
def whisper_config() -> WhisperSpeechToTextConfig:
    return WhisperSpeechToTextConfig(
        device="cuda",
        model_type="base",
        model_download_path="/tmp",
        log_level="INFO",
    )


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def whisper_worker(
    whisper_config: WhisperSpeechToTextConfig,
    mock_logger: Logger,
) -> Generator[WhisperSpeechToTextWorker, None, None]:
    worker = WhisperSpeechToTextWorker(whisper_config, mock_logger)
    yield worker
    worker.stop()


def test_transcribe_sends_correct_command(whisper_worker: WhisperSpeechToTextWorker) -> None:
    with (
        patch("multiprocessing.Process") as MockProcess,
        patch(
            "data.workers.whisper_speech_to_text_worker.whisper.load_model",
        ) as mock_load_model,
    ):
        mock_process = Mock()
        MockProcess.return_value = mock_process
        mock_model = Mock()
        mock_load_model.return_value = mock_model

        # Given
        whisper_worker.start()
        file_path = "test.wav"
        language = "en"

        # When
        with (
            patch.object(whisper_worker._pipe_parent, "send") as mock_send,
            patch.object(
                whisper_worker._pipe_parent,
                "recv",
                return_value={},
            ),
        ):
            whisper_worker.transcribe(file_path, language, {})

            # Then
            mock_send.assert_called_once_with(("transcribe", (file_path, language, {})))


def test_transcribe_raises_error_if_worker_not_running(whisper_worker: WhisperSpeechToTextWorker) -> None:
    # Given
    file_path = "test.wav"
    language = "en"

    # When / Then
    with pytest.raises(RuntimeError, match="Worker process is not running"):
        whisper_worker.transcribe(file_path, language, {})


def test_initialize_shared_object(whisper_config: WhisperSpeechToTextConfig, mock_logger: Logger) -> None:
    worker = WhisperSpeechToTextWorker(whisper_config, mock_logger)
    with patch("data.workers.whisper_speech_to_text_worker.whisper.load_model") as mock_load_model:
        mock_model = Mock()
        mock_load_model.return_value = mock_model
        mock_model.to.return_value = mock_model

        # When
        model = worker.initialize_shared_object(whisper_config)

        # Then
        mock_load_model.assert_called_once_with(
            whisper_config.model_type,
            download_root=whisper_config.model_download_path,
        )
        assert model == mock_model


def test_handle_command_transcribe(whisper_config: WhisperSpeechToTextConfig, mock_logger: Logger) -> None:
    worker = WhisperSpeechToTextWorker(whisper_config, mock_logger)
    model = Mock()
    pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()

    file_path = "test.wav"
    language = "en"
    command = "transcribe"
    args: tuple[str, str, dict[str, Any]] = (file_path, language, {})

    with patch.object(model, "transcribe", return_value={"text": "transcribed text"}):
        # When
        worker.handle_command(command, args, model, whisper_config, pipe, is_processing, processing_lock)

        # Then
        model.transcribe.assert_called_once_with(file_path, language="en", fp16=True)
        pipe.send.assert_called_once_with({"text": "transcribed text"})


def test_handle_command_transcribe_error(whisper_config: WhisperSpeechToTextConfig, mock_logger: Logger) -> None:
    worker = WhisperSpeechToTextWorker(whisper_config, mock_logger)
    model = Mock()
    pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()

    file_path = "test.wav"
    language = "en"
    command = "transcribe"
    args: tuple[str, str, dict[str, Any]] = (file_path, language, {})

    with patch.object(model, "transcribe", side_effect=RuntimeError("Transcription error")):
        # When
        worker.handle_command(command, args, model, whisper_config, pipe, is_processing, processing_lock)

        # Then
        assert pipe.send.call_count == 1
        sent_exception = pipe.send.call_args[0][0]
        assert isinstance(sent_exception, RuntimeError)
        assert str(sent_exception) == "Transcription error"
