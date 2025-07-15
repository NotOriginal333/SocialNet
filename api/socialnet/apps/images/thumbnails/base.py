from abc import ABC, abstractmethod


class ThumbnailGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, source_path: str, size: tuple = (200, 200)) -> str:
        pass
