from PIL import Image as PILImage
from pathlib import Path
from .base import ThumbnailGeneratorInterface


class PillowThumbnailGenerator(ThumbnailGeneratorInterface):
    def __init__(self, base_path: str = "media", suffix: str = "_thumb"):
        self.base_path = Path(base_path)
        self.suffix = suffix

    def generate(self, source_path: str, size=(200, 200)) -> str:
        if source_path.startswith("/media/"):
            relative_path = source_path[len("/media/"):]
        else:
            relative_path = source_path

        source_file = self.base_path / relative_path

        ext = source_file.suffix
        stem = source_file.stem

        thumb_name = f"{stem}{self.suffix}{ext}"
        thumb_path = source_file.parent / thumb_name

        with PILImage.open(source_file) as img:
            img.thumbnail(size)
            img.save(thumb_path)

        return str(Path(source_path).parent / thumb_name).replace("\\", "/")
