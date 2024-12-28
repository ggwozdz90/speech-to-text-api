import os
from typing import Optional

from dotenv import load_dotenv


class AppConfig:
    _instance: Optional["AppConfig"] = None

    device: Optional[str]
    file_upload_path: Optional[str]
    delete_files_after_transcription: Optional[bool]
    fastapi_host: Optional[str]
    fastapi_port: Optional[int]
    speach_to_text_model_name: Optional[str]
    speach_to_text_model_type: Optional[str]
    speach_to_text_model_download_path: Optional[str]
    translation_model_name: Optional[str]
    translation_model_download_path: Optional[str]
    model_idle_timeout: Optional[int]

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def load_config(self) -> None:
        load_dotenv()
        self._load_env_variables()

    def _load_env_variables(self) -> None:
        self.device = os.getenv("DEVICE", "cpu")
        self.file_upload_path = os.getenv("FILE_UPLOAD_PATH", "uploaded_files")
        self.delete_files_after_transcription = self._str_to_bool(os.getenv("DELETE_FILES_AFTER_TRANSCRIPTION", "true"))
        self.fastapi_host = os.getenv("FASTAPI_HOST", "127.0.0.1")
        self.model_idle_timeout = int(os.getenv("MODEL_IDLE_TIMEOUT", "60"))
        self.speach_to_text_model_name = os.getenv("SPEACH_TO_TEXT_MODEL_NAME", "openai/whisper")
        self.speach_to_text_model_type = os.getenv("SPEACH_TO_TEXT_MODEL_TYPE", "turbo")
        self.speach_to_text_model_download_path = os.getenv(
            "SPEACH_TO_TEXT_MODEL_DOWNLOAD_PATH", "downloaded_speach_to_text_models"
        )
        self.translation_model_name = os.getenv("TRANSLATION_MODEL_NAME", "facebook/mbart-large-50-many-to-many-mmt")
        self.translation_model_download_path = os.getenv(
            "TRANSLATION_MODEL_DOWNLOAD_PATH", "downloaded_translation_models"
        )
        try:
            self.fastapi_port = int(os.getenv("FASTAPI_PORT", "8000"))
        except ValueError:
            self.fastapi_port = 8000

    def _str_to_bool(self, value: str) -> bool:
        return value.lower() in ("true", "1", "yes")

    def print_config(self) -> None:
        print("### APP CONFIG START ###")
        print(f"DEVICE: {self.device}")
        print(f"FILE_UPLOAD_PATH: {self.file_upload_path}")
        print(f"DELETE_FILES_AFTER_TRANSCRIPTION: {self.delete_files_after_transcription}")
        print(f"FASTAPI_HOST: {self.fastapi_host}")
        print(f"FASTAPI_PORT: {self.fastapi_port}")
        print(f"SPEACH_TO_TEXT_MODEL_NAME: {self.speach_to_text_model_name}")
        print(f"SPEACH_TO_TEXT_MODEL_TYPE: {self.speach_to_text_model_type}")
        print(f"SPEACH_TO_TEXT_MODEL_DOWNLOAD_PATH: {self.speach_to_text_model_download_path}")
        print(f"TRANSLATION_MODEL_NAME: {self.translation_model_name}")
        print(f"TRANSLATION_MODEL_DOWNLOAD_PATH: {self.translation_model_download_path}")
        print(f"MODEL_IDLE_TIMEOUT: {self.model_idle_timeout}")
        print("### APP CONFIG END ###")
