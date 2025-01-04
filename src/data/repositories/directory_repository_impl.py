import os
from typing import Annotated

from fastapi import Depends

from core.logger.logger import Logger
from domain.repositories.directory_repository import DirectoryRepository


class DirectoryRepositoryImpl(DirectoryRepository):  # type: ignore
    def __init__(
        self,
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.logger = logger

    def create_directory(self, path: str) -> None:
        if not os.path.exists(path):
            self.logger.debug(f"Creating directory: {path}")
            os.makedirs(path)
