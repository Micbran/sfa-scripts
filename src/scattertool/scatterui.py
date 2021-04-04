from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from pymel.core.system import Path


def return_maya_main_window():
	main_window = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
	def __init__(self):
		super(ScatterToolUI, self).__init__(parent=return_maya_main_window())
		self.setWindowTitle("Scatter Tool I")
		self.setMinimumWidth(500)
		self.setMinimumHeight(200)
		self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

		self._create_ui()
		self._create_connections()

	def _create_ui(self):
		pass

	def _create_connections(self):
		pass
