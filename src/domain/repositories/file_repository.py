from abc import ABC, abstractmethod

from fastapi import UploadFile


class FileRepository(ABC):
    @abstractmethod
    async def save_file(self, file: UploadFile) -> str:
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> None:
        pass
