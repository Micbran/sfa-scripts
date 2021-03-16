from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from pymel.core.system import Path

from scenefile import SceneFile


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
		self._create_ui()

	def _create_ui(self):
		self.main_layout = QtWidgets.QVBoxLayout()
		self.first_row_layout = self._create_folder_ui()
		self.file_input_layout = self._create_file_input_ui()

		self.title_label = QtWidgets.QLabel("Smart Save")
		self.title_label.setStyleSheet("font: bold 20px;")

		self.main_layout.addWidget(self.title_label)
		self.main_layout.addLayout(self.first_row_layout)
		self.main_layout.addLayout(self.file_input_layout)

		self.setLayout(self.main_layout)

	def _create_folder_ui(self):
		default_folder = Path(cmds.workspace(rootDirectory=True, query=True))
		default_folder = default_folder / "scenes"
		self.folder_line_edit = QtWidgets.QLineEdit(default_folder)
		self.folder_browse_button = QtWidgets.QPushButton("...")
		folder_layout = QtWidgets.QHBoxLayout()
		folder_layout.addWidget(self.folder_line_edit)
		folder_layout.addWidget(self.folder_browse_button)
		return folder_layout

	def _create_file_input_ui(self):
		file_input_layout = self._create_filename_headers()

		self.descriptor_line_edit = QtWidgets.QLineEdit("main")
		self.descriptor_line_edit.setMinimumWidth(100)
		self.task_line_edit = QtWidgets.QLineEdit("model")
		self.task_line_edit.setFixedWidth(50)
		self.version_spinbox = QtWidgets.QSpinBox()
		self.version_spinbox.setValue(1)
		self.version_spinbox.setFixedWidth(50)
		self.version_spinbox.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
		self.extension_label = QtWidgets.QLabel(".ma")

		file_input_layout.addWidget(self.descriptor_line_edit, 1, 0)
		file_input_layout.addWidget(QtWidgets.QLabel("_"), 1, 1)
		file_input_layout.addWidget(self.task_line_edit, 1, 2)
		file_input_layout.addWidget(QtWidgets.QLabel("_"), 1, 3)
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




