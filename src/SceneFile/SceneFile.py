from pathlib import Path


class SceneFile:
    def __init__(self, folder_path: str, descriptor: str, task: str, version: int, extension: str):
        self.folder_path = Path(folder_path)
        self.descriptor = descriptor
        self.task = task
        self.version = version
        self.extension = extension

    @property
    def file_name(self) -> str:
        return "{descriptor}_{task}_v{version}.{extension}"\
            .format(descriptor=self.descriptor, task=self.task, version=self.version, extension=self.extension)

    @property
    def path(self) -> Path:
        return self.folder_path / self.file_name
