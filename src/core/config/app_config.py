import os
from typing import Optional

from dotenv import load_dotenv

from core.logger.logger import Logger


class AppConfig:
    _instance: Optional["AppConfig"] = None

    log_level: Optional[str]
    device: Optional[str]
    file_upload_path: Optional[str]
    delete_files_after_transcription: Optional[bool]
    fastapi_host: Optional[str]
    fastapi_port: Optional[int]
    speech_to_text_model_name: Optional[str]
    speech_to_text_model_type: Optional[str]
    speech_to_text_model_download_path: Optional[str]
    translation_model_name: Optional[str]
    translation_model_download_path: Optional[str]
    model_idle_timeout: Optional[int]

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)

        return cls._instance

    def _str_to_bool(self, value: str) -> bool:
        return value.lower() in ("true", "1", "yes")

    def _load_env_variables(self) -> None:
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.device = os.getenv("DEVICE", "cpu")
        self.file_upload_path = os.getenv("FILE_UPLOAD_PATH", "uploaded_files")
        self.delete_files_after_transcription = self._str_to_bool(os.getenv("DELETE_FILES_AFTER_TRANSCRIPTION", "true"))
        self.fastapi_host = os.getenv("FASTAPI_HOST", "127.0.0.1")
        self.model_idle_timeout = int(os.getenv("MODEL_IDLE_TIMEOUT", "60"))
        self.speech_to_text_model_name = os.getenv("SPEECH_TO_TEXT_MODEL_NAME", "openai/whisper")
        self.speech_to_text_model_type = os.getenv("SPEECH_TO_TEXT_MODEL_TYPE", "turbo")
        self.speech_to_text_model_download_path = os.getenv(
            "SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH",
            "downloaded_speech_to_text_models",
        )
        self.translation_model_name = os.getenv("TRANSLATION_MODEL_NAME", "facebook/mbart-large-50-many-to-many-mmt")
        self.translation_model_download_path = os.getenv(
            "TRANSLATION_MODEL_DOWNLOAD_PATH",
            "downloaded_translation_models",
        )
        try:
            self.fastapi_port = int(os.getenv("FASTAPI_PORT", "8000"))
        except ValueError:
            self.fastapi_port = 8000

    def initialize(
        self,
        logger: Logger,
    ) -> None:
        logger.info("Initializing configuration...")
        load_dotenv()
        self._load_env_variables()
        config_message = (
            f"Configuration loaded:\n"
            f"LOG_LEVEL: {self.log_level}\n"
            f"DEVICE: {self.device}\n"
            f"FILE_UPLOAD_PATH: {self.file_upload_path}\n"
            f"DELETE_FILES_AFTER_TRANSCRIPTION: {self.delete_files_after_transcription}\n"
            f"FASTAPI_HOST: {self.fastapi_host}\n"
            f"FASTAPI_PORT: {self.fastapi_port}\n"
            f"SPEECH_TO_TEXT_MODEL_NAME: {self.speech_to_text_model_name}\n"
            f"SPEECH_TO_TEXT_MODEL_TYPE: {self.speech_to_text_model_type}\n"
            f"SPEECH_TO_TEXT_MODEL_DOWNLOAD_PATH: {self.speech_to_text_model_download_path}\n"
            f"TRANSLATION_MODEL_NAME: {self.translation_model_name}\n"
            f"TRANSLATION_MODEL_DOWNLOAD_PATH: {self.translation_model_download_path}\n"
            f"MODEL_IDLE_TIMEOUT: {self.model_idle_timeout}"
        )
        logger.info(config_message)
        logger.info("Configuration initialized successfully.")
