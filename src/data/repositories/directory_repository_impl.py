import os

from domain.repositories.directory_repository import DirectoryRepository


class DirectoryRepositoryImpl(DirectoryRepository):  # type: ignore
    def create_directory(self, path: str) -> None:
        if not os.path.exists(path):
            os.makedirs(path)
