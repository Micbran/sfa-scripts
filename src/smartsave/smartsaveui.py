from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
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
