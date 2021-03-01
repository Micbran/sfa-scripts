from pathlib import Path


class SceneFile:
    def __init__(self, path: str):
        self.folder_path: Path = Path()
        self.descriptor: str = "DEFAULT"
        self.task: str = "DEFAULT"
        self.version: int = 0
        self.extension: str = ".DEFAULT"
        self._init_from_path(Path(path))

    def _init_from_path(self, path: Path):
        self.folder_path = path.parent
        self.extension = path.suffix
        self.descriptor, self.task, version = path.stem.split("_")
        self.version = int(version[1:])

    @property
    def file_name(self) -> str:
        return "{descriptor}_{task}_v{version:03d}{extension}"\
            .format(descriptor=self.descriptor, task=self.task, version=self.version, extension=self.extension)

    @property
    def path(self) -> Path:
        return self.folder_path / self.file_name
