from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from pymel.core.system import Path

from scenefile import SceneFile
from qtextensions import PaddedQSpinBox


def return_maya_main_window():
	main_window = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window), QtWidgets.QWidget)


class SmartSaveUI(QtWidgets.QDialog):
	def __init__(self):
		super(SmartSaveUI, self).__init__(parent=return_maya_main_window())
		self.setWindowTitle("SmartSave Tool")
		self.setMinimumWidth(500)
		self.setMaximumHeight(200)
		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

		self.scenefile = SceneFile()
		self._create_ui()
		self._create_connections()

	def _create_ui(self):
		self.main_layout = QtWidgets.QVBoxLayout()
		self.folder_row_layout = self._create_folder_ui()
		self.file_input_layout = self._create_file_input_ui()
		self.button_layout = self._create_save_ui()

		self.title_label = QtWidgets.QLabel("Smart Save")
		self.title_label.setStyleSheet("font: bold 20px;")

		self.main_layout.addWidget(self.title_label)
		self.main_layout.addLayout(self.folder_row_layout)
		self.main_layout.addLayout(self.file_input_layout)
		self.main_layout.addStretch()
		self.main_layout.addLayout(self.button_layout)

		self.setLayout(self.main_layout)

	def _create_folder_ui(self):
		self.folder_line_edit = QtWidgets.QLineEdit(self.scenefile.folder_path)
		self.folder_browse_button = QtWidgets.QPushButton("...")
		folder_layout = QtWidgets.QHBoxLayout()
		folder_layout.addWidget(self.folder_line_edit)
		folder_layout.addWidget(self.folder_browse_button)
		return folder_layout

	def _create_file_input_ui(self):
		file_input_layout = self._create_filename_headers()

		self.descriptor_line_edit = QtWidgets.QLineEdit(self.scenefile.descriptor)
		self.descriptor_line_edit.setMinimumWidth(100)
		self.task_line_edit = QtWidgets.QLineEdit(self.scenefile.task)
		self.task_line_edit.setFixedWidth(50)
		self.version_spinbox = PaddedQSpinBox()
		self.version_spinbox.setValue(self.scenefile.version)
		self.version_spinbox.setFixedWidth(50)
		self.version_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
		self.version_spinbox.setMaximum(999)
		self.extension_label = QtWidgets.QLabel(".ma")

		file_input_layout.addWidget(self.descriptor_line_edit, 1, 0)
		file_input_layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
		file_input_layout.addWidget(self.task_line_edit, 1, 2)
		file_input_layout.addWidget(QtWidgets.QLabel("_v"), 1, 3)
		file_input_layout.addWidget(self.version_spinbox, 1, 4)
		file_input_layout.addWidget(self.extension_label, 1, 5)
		return file_input_layout

	def _create_filename_headers(self):
		self.descriptor_header_label = QtWidgets.QLabel("Descriptor")
		self.descriptor_header_label.setStyleSheet("font: bold;")
		self.task_header_label = QtWidgets.QLabel("Task")
		self.task_header_label.setStyleSheet("font: bold;")
		self.version_header_label = QtWidgets.QLabel("Version")
		self.version_header_label.setStyleSheet("font: bold;")
		file_label_layout = QtWidgets.QGridLayout()
		file_label_layout.addWidget(self.descriptor_header_label, 0, 0)
		file_label_layout.addWidget(self.task_header_label, 0, 2)
		file_label_layout.addWidget(self.version_header_label, 0, 4)
		return file_label_layout

	def _create_save_ui(self):
		self.save_button = QtWidgets.QPushButton("Save")
		self.save_increment_button = QtWidgets.QPushButton("Save Increment")
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addWidget(self.save_button)
		button_layout.addWidget(self.save_increment_button)
		return button_layout

	def _create_connections(self):
		self.folder_browse_button.clicked.connect(self._do_browse_dir)
		self.save_button.clicked.connect(self._do_save)
		self.save_increment_button.clicked.connect(self._do_increment_save)

	@QtCore.Slot()
	def _do_browse_dir(self):
		directory = QtWidgets.QFileDialog.getExistingDirectory(
			self, caption="Select Directory",
			dir=self.folder_line_edit.text(),
			options=QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks)
		self.folder_line_edit.setText(directory)

	@QtCore.Slot()
	def _do_save(self):
		self._update_scene_file_from_fields()
		self.scenefile.save_file()

	@QtCore.Slot()
	def _do_increment_save(self):
		self._update_scene_file_from_fields()
		self.scenefile.increment_save_file()
		self.version_spinbox.setValue(self.scenefile.version)

	def _update_scene_file_from_fields(self):
		self.scenefile.folder_path = str(self.folder_line_edit.text())
		self.scenefile.descriptor = str(self.descriptor_line_edit.text())
		self.scenefile.task = str(self.task_line_edit.text())
		self.scenefile.extension = str(self.extension_label.text())
		self.scenefile.version = int(self.version_spinbox.value())

