import logging
from pymel.core.system import Path
import pymel.core as pmc

log = logging.getLogger(__name__)


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

    def save_file(self):
        try:
            return pmc.system.saveAs(self.path)
        except RuntimeError as err:
            log.warning("Missing directories in path, creating directories...")
            self.folder_path.makedirs_p()
            return pmc.system.saveAs(self.path)




