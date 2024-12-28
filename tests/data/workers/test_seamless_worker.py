import multiprocessing
from unittest.mock import MagicMock, Mock, patch

import pytest
from transformers import AutoProcessor, SeamlessM4Tv2ForTextToText

from src.data.workers.seamless_worker import SeamlessConfig, SeamlessWorker


@pytest.fixture
def mock_config() -> SeamlessConfig:
    return SeamlessConfig(
        device="cpu", model_name="facebook/seamless-m4t-v2-large", model_download_path="/path/to/model"
    )


@pytest.fixture
def mock_worker(mock_config: SeamlessConfig) -> SeamlessWorker:
    worker = SeamlessWorker(config=mock_config)
    worker._pipe_parent = Mock()
    return worker


def test_translate_success(mock_worker: SeamlessWorker) -> None:
    # Given
    mock_worker.is_alive = Mock(return_value=True)
    mock_worker._pipe_parent.recv = Mock(return_value="translated text")

    # When
    result = mock_worker.translate("hello", "en", "fr")

    # Then
    assert result == "translated text"
    mock_worker._pipe_parent.send.assert_called_once_with(("translate", ("hello", "en", "fr")))


def test_translate_worker_not_running(mock_worker: SeamlessWorker) -> None:
    # Given
    mock_worker.is_alive = Mock(return_value=False)

    # When / Then
    with pytest.raises(RuntimeError, match="Worker process is not running"):
        mock_worker.translate("hello", "en", "fr")


def test_translate_exception(mock_worker: SeamlessWorker) -> None:
    # Given
    mock_worker.is_alive = Mock(return_value=True)
    mock_worker._pipe_parent.recv = Mock(return_value=Exception("Translation error"))

    # When / Then
    with pytest.raises(Exception, match="Translation error"):
        mock_worker.translate("hello", "en", "fr")


def test_initialize_shared_object(mock_config: SeamlessConfig) -> None:
    # Given
    with patch.object(SeamlessM4Tv2ForTextToText, "from_pretrained") as mock_model, patch.object(
        AutoProcessor, "from_pretrained"
    ) as mock_processor:
        mock_model.return_value = MagicMock()
        mock_processor.return_value = MagicMock()

        worker = SeamlessWorker(config=mock_config)

        # When
        model, processor = worker.initialize_shared_object(mock_config)

        # Then
        mock_model.assert_called_once_with(mock_config.model_name, cache_dir=mock_config.model_download_path)
        mock_processor.assert_called_once_with(mock_config.model_name, cache_dir=mock_config.model_download_path)
        assert model is not None
        assert processor is not None


def test_handle_command_translate_success(mock_worker: SeamlessWorker, mock_config: SeamlessConfig) -> None:
    # Given
    mock_pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()
    mock_model = MagicMock()
    mock_processor = MagicMock()
    mock_processor.decode.return_value = "translated text"

    # When
    mock_worker.handle_command(
        "translate",
        ("hello", "en", "fr"),
        (mock_model, mock_processor),
        mock_config,
        mock_pipe,
        is_processing,
        processing_lock,
    )

    # Then
    mock_pipe.send.assert_called_once_with("translated text")


def test_handle_command_translate_exception(mock_worker: SeamlessWorker, mock_config: SeamlessConfig) -> None:
    # Given
    mock_pipe = Mock()
    is_processing = multiprocessing.Value("b", False)
    processing_lock = multiprocessing.Lock()
    mock_model = MagicMock()
    mock_processor = MagicMock()
    mock_processor.decode.side_effect = RuntimeError("Decoding error")

    # When
    mock_worker.handle_command(
        "translate",
        ("hello", "en", "fr"),
        (mock_model, mock_processor),
        mock_config,
        mock_pipe,
        is_processing,
        processing_lock,
    )

    # Then
    assert mock_pipe.send.call_count == 1
    sent_exception = mock_pipe.send.call_args[0][0]
    assert isinstance(sent_exception, RuntimeError)
    assert str(sent_exception) == "Decoding error"
