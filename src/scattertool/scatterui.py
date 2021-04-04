from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from pymel.core.system import Path
import constants
from scatter_instance import ScatterInstance


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
        self.main_layout = QtWidgets.QVBoxLayout()
        self.selection_layout = self._create_selection_ui()
        self.scale_layout = self._create_scale_ui()
        self.rotation_layout = self._create_rotation_ui()
        self.button_layout = self._create_button_ui()

        self.title_label = QtWidgets.QLabel("Scatter Tool")
        self.title_label.setStyleSheet("font: bold 20px;")
        self.main_layout.addWidget(self.title_label)

        self.main_layout.addLayout(self.selection_layout)
        self.main_layout.addLayout(self.scale_layout)
        self.main_layout.addLayout(self.rotation_layout)
        self.main_layout.addStretch()
        self.main_layout.addLayout(self.button_layout)

    def _create_selection_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_scale_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_rotation_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_button_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_connections(self):
        pass

    @QtCore.Slot()
    def _get_current_select_single_object(self):
        pass

    @QtCore.Slot()
    def _get_current_select_multi_object_vertex(self):
        pass

    @QtCore.Slot()
    def _do_scatter(self):
        scatter = self._create_scatter_instance_from_fields()
        scatter.scatter_on_source()

    def _update_scatter_instance_from_fields(self):
        scale_ranges = (float(self.scale_x_edit.text()),
                        float(self.scale_y_edit.text()),
                        float(self.scale_z_edit.text()))
        rotation_ranges = (float(self.rotation_x_edit.text()),
                           float(self.rotation_y_edit.text()),
                           float(self.rotation_z_edit.text()))
        source_object = str(self.source_object_edit.text())
        destinations = self.destinations
        return ScatterInstance(source_object, destinations,
                               scale_ranges, rotation_ranges)

