import os
from typing import Annotated

from fastapi import Depends, UploadFile

from config.app_config import AppConfig


class FileService:
    def __init__(
        self,
        config: Annotated[AppConfig, Depends()],
    ) -> None:
        self.config = config

    async def save_file(
        self,
        file: UploadFile,
    ) -> str:
        file_path = os.path.join(self.config.file_upload_path, file.filename or "unknown")
        normalized_file_path = os.path.normpath(file_path)
        normalized_file_upload_path = os.path.normpath(self.config.file_upload_path)
        absolute_path = os.path.abspath(normalized_file_path)

        if not normalized_file_path.startswith(normalized_file_upload_path):
            raise Exception("Invalid file name")

        with open(absolute_path, "wb") as f:
            while content := await file.read(1024 * 1024):  # 1MB chunks
                f.write(content)

        return absolute_path

    def delete_file(
        self,
        path: str,
    ) -> None:
        normalized_path = os.path.normpath(path)
        normalized_file_upload_path = os.path.normpath(self.config.file_upload_path)
        absolute_path = os.path.abspath(normalized_path)

        if normalized_file_upload_path not in absolute_path:
            raise Exception("Invalid file path")

        os.remove(absolute_path)
