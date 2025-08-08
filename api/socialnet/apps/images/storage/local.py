import os
from pathlib import Path

from .base import ImageStorageInterface


class LocalImageStorage(ImageStorageInterface):
    def __init__(self, base_path: str, base_url: str):
        self.base_path = Path(base_path)
        self.base_url = base_url

    def save(self, file_obj, filename):
        full_path = self.base_path / filename
        full_path.parent.mkdir(parents=True, exist_ok=True)

        file_obj.seek(0)
        with open(full_path, 'wb') as f:
            f.write(file_obj.read())

        return str(Path(self.base_url) / filename).replace('\\', '/')

    def delete(self, filename):
        try:
            os.remove(self.base_path / filename)
        except FileNotFoundError:
            pass

    def get(self, filename):
        with open(self.base_path / filename, 'rb') as f:
            return f.read()
