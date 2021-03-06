from pymel.core.system import Path


class SceneFile:
    def __init__(self, path):
        self.folder_path = Path()
        self.descriptor = "DEFAULT"
        self.task = "DEFAULT"
        self.version = 0
        self.extension = ".DEFAULT"
        self._init_from_path(Path(path))

    def _init_from_path(self, path):
        self.folder_path = path.parent
        self.extension = path.ext
        self.descriptor, self.task, version = path.name.stripext().split("_")
        self.version = int(version[1:])

    @property
    def file_name(self):
        return "{descriptor}_{task}_v{version:03d}{extension}"\
            .format(descriptor=self.descriptor, task=self.task, version=self.version, extension=self.extension)

    @property
    def path(self):
        return self.folder_path / self.file_name


scene_file = SceneFile("D:/Programming/EighthSemester/Scripting/sfa-scripts/src/tankmodel_mayaintro_v001.ma")
print(scene_file.folder_path)
print(scene_file.descriptor)
print(scene_file.task)
print(scene_file.version)
print(scene_file.extension)
print(scene_file.file_name)
print(scene_file.path)