import logging
from pymel.core.system import Path
import pymel.core as pmc
import maya.cmds as cmds

log = logging.getLogger(__name__)


class SceneFile(object):
	def __init__(self, path=None):
		self._folder_path = Path(cmds.workspace(query=True, rootDirectory=True)) / "scenes"
		self.descriptor = "DEFAULT"
		self.task = "DEFAULT"
		self.version = 0
		self.extension = ".ma"
		scene = pmc.system.sceneName()
		if not path and scene:
			path = scene
		elif not path and not scene:
			log.info("Initialized SceneFile object with default properties.")
			return
		self._init_from_path(Path(path))

	def _init_from_path(self, path):
		self.folder_path = path.parent
		self.extension = path.ext
		self.descriptor, self.task, version = path.name.stripext().split("_")
		self.version = int(version[1:])

	@property
	def folder_path(self):
		return self._folder_path

	@folder_path.setter
	def folder_path(self, value):
		self._folder_path = Path(value)

	@property
	def file_name(self):
		return "{descriptor}_{task}_v{version:03d}{extension}" \
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

	def increment_save_file(self):
		self.version = self._next_available_version()
		return self.save_file()

	def _next_available_version(self):
		search_pattern = "{descriptor}_{task}_v*{extension}" \
			.format(descriptor=self.descriptor, task=self.task, extension=self.extension)

		matched_scenefiles = []
		for file_path in self.folder_path.files():
			if file_path.name.fnmatch(search_pattern):
				matched_scenefiles.append(file_path)

		if not matched_scenefiles:
			return 1
		matched_scenefiles.sort(reverse=True)
		latest_scenefile = matched_scenefiles[0]
		latest_version = int(latest_scenefile.name.stripext().split("_v")[-1])
		return latest_version + 1
