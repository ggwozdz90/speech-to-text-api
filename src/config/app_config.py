import os
from typing import Optional

from dotenv import load_dotenv


class AppConfig:
    _instance: Optional["AppConfig"] = None

    file_upload_path: Optional[str]
    delete_files_after_transcription: Optional[bool]
    fastapi_host: Optional[str]
    fastapi_port: Optional[int]
    whisper_model_name: Optional[str]
    whisper_model_download_path: Optional[str]

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def load_config(self) -> None:
        load_dotenv()
        self._load_env_variables()

    def _load_env_variables(self) -> None:
        self.file_upload_path = os.getenv("FILE_UPLOAD_PATH", "uploaded_files")
        self.delete_files_after_transcription = self._str_to_bool(os.getenv("DELETE_FILES_AFTER_TRANSCRIPTION", "true"))
        self.fastapi_host = os.getenv("FASTAPI_HOST", "127.0.0.1")
        self.whisper_model_name = os.getenv("WHISPER_MODEL_NAME", "turbo")
        self.whisper_model_download_path = os.getenv("WHISPER_MODEL_DOWNLOAD_PATH", "downloaded_whisper_models")
        try:
            self.fastapi_port = int(os.getenv("FASTAPI_PORT", "8000"))
        except ValueError:
            self.fastapi_port = 8000

    def _str_to_bool(self, value: str) -> bool:
        return value.lower() in ("true", "1", "yes")

    def print_config(self) -> None:
        print("### APP CONFIG START ###")
        print(f"FILE_UPLOAD_PATH: {self.file_upload_path}")
        print(f"DELETE_FILES_AFTER_TRANSCRIPTION: {self.delete_files_after_transcription}")
        print(f"FASTAPI_HOST: {self.fastapi_host}")
        print(f"FASTAPI_PORT: {self.fastapi_port}")
        print(f"WHISPER_MODEL_NAME: {self.whisper_model_name}")
        print(f"WHISPER_MODEL_DOWNLOAD_PATH: {self.whisper_model_download_path}")
        print("### APP CONFIG END ###")
