from PySide2 import QtWidgets
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance
from scenefile import SceneFile


def return_maya_main_window():
	main_window = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window), QtWidgets.QWidget)


class SimpleUI(QtWidgets.QDialog):

	def __init__(self):
		super(SimpleUI, self).__init__(parent=return_maya_main_window())
		self.setWindowTitle("A Simple UI")