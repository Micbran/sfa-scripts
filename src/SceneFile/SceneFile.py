from os import path


class SceneFile(object):
    def __init__(self, folder_path, descriptor, task, version, extension):
        self.folder_path = folder_path
        self.descriptor = descriptor
        self.task = task
        self.version = version
        self.extension = extension

    @property
    def file_name(self):
        return "{0}_{1}_v{2}.{3}"\
            .format(self.descriptor, self.task, self.version, self.extension)

    @property
    def path(self):
        return path.join(self.folder_path, self.file_name)
