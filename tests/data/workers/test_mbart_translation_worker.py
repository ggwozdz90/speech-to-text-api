import multiprocessing
from typing import Generator
from unittest.mock import Mock, patch

import pytest
import torch

from core.logger.logger import Logger
from data.workers.mbart_translation_worker import (
    MBartTranslationConfig,
    MBartTranslationWorker,
)


@pytest.fixture
def mock_tensor() -> Mock:
    return Mock(spec=torch.Tensor)


@pytest.fixture
def mbart_config() -> MBartTranslationConfig:
    return MBartTranslationConfig(
        device="cuda",
        model_name="facebook/mbart-large-50",
        model_download_path="/tmp",
        log_level="INFO",
    )


@pytest.fixture
def mock_logger() -> Logger:
    return Mock(Logger)


@pytest.fixture
def mbart_worker(
    mbart_config: MBartTranslationConfig,
    mock_logger: Logger,
) -> Generator[MBartTranslationWorker, None, None]:
    worker = MBartTranslationWorker(mbart_config, mock_logger)
    yield worker
    worker.stop()


class MockTensor:
    def to(self, device: str) -> "MockTensor":
        return self


def test_translate_sends_correct_command(mbart_worker: MBartTranslationWorker) -> None:
    with (
        patch("multiprocessing.Process") as MockProcess,
        patch(
            "data.workers.mbart_translation_worker.AutoModelForSeq2SeqLM.from_pretrained",
        ) as mock_load_model,
        patch(
            "data.workers.mbart_translation_worker.AutoTokenizer.from_pretrained",
        ) as mock_load_tokenizer,
    ):
        mock_process = Mock()
        MockProcess.return_value = mock_process
        mock_model = Mock()
        mock_tokenizer = Mock()
        mock_load_model.return_value = mock_model
        mock_load_tokenizer.return_value = mock_tokenizer

        # Given
        mbart_worker.start()
        text = "Hello, world!"
        source_language = "en"
        target_language = "fr"

        # When
        with (
            patch.object(mbart_worker._pipe_parent, "send") as mock_send,
            patch.object(
                mbart_worker._pipe_parent,
                "recv",
                return_value="Bonjour, le monde!",
            ),
        ):
            mbart_worker.translate(text, source_language, target_language)

            # Then
            mock_send.assert_called_once_with(("translate", (text, source_language, target_language)))


def test_translate_raises_error_if_worker_not_running(mbart_worker: MBartTranslationWorker) -> None:
    # Given
    text = "Hello, world!"
    source_language = "en"
    target_language = "fr"

    # When / Then
    with pytest.raises(RuntimeError, match="Worker process is not running"):
        mbart_worker.translate(text, source_language, target_language)


def test_initialize_shared_object(mbart_config: MBartTranslationConfig, mock_logger: Logger) -> None:
    worker = MBartTranslationWorker(mbart_config, mock_logger)
    with (
        patch("data.workers.mbart_translation_worker.AutoModelForSeq2SeqLM.from_pretrained") as mock_load_model,
        patch(
            "data.workers.mbart_translation_worker.AutoTokenizer.from_pretrained",
        ) as mock_load_tokenizer,
    ):
        mock_model = Mock()
        mock_tokenizer = Mock()
        mock_load_model.return_value = mock_model
        mock_model.to.return_value = mock_model
        mock_load_tokenizer.return_value = mock_tokenizer

        # When
        model, tokenizer = worker.initialize_shared_object(mbart_config)

        # Then
        mock_load_model.assert_called_once_with(
            mbart_config.model_name,
            cache_dir=mbart_config.model_download_path,
        )
        mock_load_tokenizer.assert_called_once_with(
            mbart_config.model_name,
            cache_dir=mbart_config.model_download_path,
        )
        assert model == mock_model
        assert tokenizer == mock_tokenizer


def test_handle_command_translate(mbart_worker: MBartTranslationWorker, mbart_config: MBartTranslationConfig) -> None:
    with (
        patch("data.workers.mbart_translation_worker.AutoModelForSeq2SeqLM.from_pretrained") as mock_load_model,
        patch(
            "data.workers.mbart_translation_worker.AutoTokenizer.from_pretrained",
        ) as mock_load_tokenizer,
        patch("torch.no_grad"),
    ):
        mock_model = Mock()
        mock_tokenizer = Mock()
        mock_load_model.return_value = mock_model
        mock_load_tokenizer.return_value = mock_tokenizer
        mock_tokenizer.lang_code_to_id = {"fr": 1}
        mock_is_processing = multiprocessing.Value("b", False)
        mock_processing_lock = multiprocessing.Lock()
        pipe = Mock()
        mock_input_tensors = {"input_ids": MockTensor(), "attention_mask": MockTensor()}
        mock_tokenizer.return_value = mock_input_tensors
        mock_generated_tokens = torch.tensor([[4, 5, 6]])
        mock_model.generate.return_value = mock_generated_tokens
        mock_tokenizer.decode.return_value = "Bonjour, le monde!"

        # When
        mbart_worker.handle_command(
            command="translate",
            args=("Hello, world!", "en", "fr"),
            shared_object=(mock_model, mock_tokenizer),
            config=mbart_config,
            pipe=pipe,
            is_processing=mock_is_processing,
            processing_lock=mock_processing_lock,
        )

        # Then
        assert not mock_is_processing.value
        mock_tokenizer.assert_called_once_with(
            ["Hello, world!"],
            truncation=True,
            padding=True,
            max_length=1024,
            return_tensors="pt",
        )
        mock_model.generate.assert_called_once_with(**mock_input_tensors, num_beams=5, forced_bos_token_id=1)
        pipe.send.assert_called_once_with("Bonjour, le monde!")


def test_handle_command_translate_error(
    mbart_worker: MBartTranslationWorker,
    mbart_config: MBartTranslationConfig,
) -> None:
    with (
        patch("data.workers.mbart_translation_worker.AutoModelForSeq2SeqLM.from_pretrained") as mock_load_model,
        patch(
            "data.workers.mbart_translation_worker.AutoTokenizer.from_pretrained",
        ) as mock_load_tokenizer,
        patch("torch.no_grad"),
    ):
        mock_model = Mock()
        mock_tokenizer = Mock()
        mock_load_model.return_value = mock_model
        mock_load_tokenizer.return_value = mock_tokenizer
        mock_tokenizer.lang_code_to_id = {"fr": 1}
        mock_is_processing = multiprocessing.Value("b", False)
        mock_processing_lock = multiprocessing.Lock()
        pipe = Mock()
        mock_input_tensors = {"input_ids": MockTensor(), "attention_mask": MockTensor()}
        mock_tokenizer.return_value = mock_input_tensors
        mock_model.generate.side_effect = RuntimeError("Translation error")

        # When
        mbart_worker.handle_command(
            command="translate",
            args=("Hello, world!", "en", "fr"),
            shared_object=(mock_model, mock_tokenizer),
            config=mbart_config,
            pipe=pipe,
            is_processing=mock_is_processing,
            processing_lock=mock_processing_lock,
        )

        # Then
        assert not mock_is_processing.value
        assert pipe.send.call_count == 1
        assert isinstance(pipe.send.call_args[0][0], RuntimeError)
        assert pipe.send.call_args[0][0].args[0] == "Translation error"
