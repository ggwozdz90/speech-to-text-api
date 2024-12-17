from abc import ABC, abstractmethod


class DirectoryRepository(ABC):
    @abstractmethod
    def create_directory(self, path: str) -> None:
        pass
