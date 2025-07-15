from abc import ABC, abstractmethod


class ImageStorageInterface(ABC):
    @abstractmethod
    def save(self, file_obj, filename) -> str:
        pass

    @abstractmethod
    def delete(self, filename):
        pass

    @abstractmethod
    def get(self, filename):
        pass
