from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
from pymel.core.system import Path
from scatter_instance import ScatterInstance

MIN_SCALE = 1.0
MIN_ROTATION = 0
MAX_ROTATION = 360


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
        self.source_label = QtWidgets.QLabel("Scatter Source")
        self.source_label.setStyleSheet("font: bold;")
        self.destination_label = QtWidgets.QLabel("Scatter Destination")
        self.destination_label.setStyleSheet("font: bold;")

        self.source_line_edit = QtWidgets.QLineEdit()
        self.source_line_edit.setMinimumWidth(100)
        self.destination_text_box = QtWidgets.QTextEdit()
        self.destination_text_box.setMinimumWidth(150)
        self.destination_text_box.setMinimumHeight(50)

        self.source_select_button = QtWidgets.QPushButton("Select")
        self.source_select_button.setMaximumWidth(75)
        self.destination_select_button = QtWidgets.QPushButton("Select")
        self.destination_select_button.setMaximumWidth(75)

        selection_grid = QtWidgets.QGridLayout()
        selection_grid.addWidget(self.source_label, 0, 0)
        selection_grid.addWidget(self.destination_label, 0, 2)
        selection_grid.addWidget(self.source_line_edit, 1, 0)
        selection_grid.addWidget(self.destination_text_box, 1, 2)
        selection_grid.addWidget(self.source_select_button, 1, 1)
        selection_grid.addWidget(self.destination_select_button, 1, 3)
        return selection_grid

    def _create_scale_ui(self):
        self.scale_label = QtWidgets.QLabel("Scale Ranges")
        self.scale_label.setStyleSheet("font: bold;")

        self.scale_x_label = QtWidgets.QLabel("X: ")
        self.scale_x_label.setStyleSheet("font: bold;")
        self.scale_y_label = QtWidgets.QLabel("Y: ")
        self.scale_y_label.setStyleSheet("font: bold;")
        self.scale_z_label = QtWidgets.QLabel("Z: ")
        self.scale_z_label.setStyleSheet("font: bold;")

        self.scale_square_label = QtWidgets.QLabel("Square Scale")
        self.scale_square_label.setStyleSheet("font: bold;")
        self.scale_xyz_label = QtWidgets.QLabel("XYZ: ")
        self.scale_xyz_label.setStyleSheet("font: bold;")
        
        self.dash_label = QtWidgets.QLabel("-")

        self.scale_x_min = QtWidgets.QLineEdit()
        self.scale_x_min.setMaximumWidth(50)
        self.scale_x_max = QtWidgets.QLineEdit()
        self.scale_x_max.setMaximumWidth(50)

        self.scale_y_min = QtWidgets.QLineEdit()
        self.scale_y_min.setMaximumWidth(50)
        self.scale_y_max = QtWidgets.QLineEdit()
        self.scale_y_max.setMaximumWidth(50)

        self.scale_z_min = QtWidgets.QLineEdit()
        self.scale_z_min.setMaximumWidth(50)
        self.scale_z_max = QtWidgets.QLineEdit()
        self.scale_z_max.setMaximumWidth(50)

        self.scale_square_min = QtWidgets.QLineEdit()
        self.scale_square_min.setMaximumWidth(50)
        self.scale_square_min.setDisabled(True)
        self.scale_square_max = QtWidgets.QLineEdit()
        self.scale_square_max.setMaximumWidth(50)
        self.scale_square_max.setDisabled(True)

        self.scale_square_checkbox = QtWidgets.QCheckBox()

        scale_grid = QtWidgets.QGridLayout()
        scale_grid.addWidget(self.scale_label, 0, 0)

        scale_grid.addWidget(self.scale_x_label, 1, 0)
        scale_grid.addWidget(self.scale_x_min, 1, 1)
        scale_grid.addWidget(self.dash_label, 1, 2)
        scale_grid.addWidget(self.scale_x_max, 1, 3)

        scale_grid.addWidget(self.scale_y_label, 2, 0)
        scale_grid.addWidget(self.scale_y_min, 2, 1)
        scale_grid.addWidget(self.dash_label, 2, 2)
        scale_grid.addWidget(self.scale_y_max, 2, 3)

        scale_grid.addWidget(self.scale_z_label, 3, 0)
        scale_grid.addWidget(self.scale_z_min, 3, 1)
        scale_grid.addWidget(self.dash_label, 3, 2)
        scale_grid.addWidget(self.scale_z_max, 3, 3)

        scale_grid.addWidget(self.scale_square_label, 4, 0)
        scale_grid.addWidget(self.scale_square_checkbox, 4, 1)

        scale_grid.addWidget(self.scale_square_label, 5, 0)
        scale_grid.addWidget(self.scale_square_min, 5, 1)
        scale_grid.addWidget(self.dash_label, 5, 2)
        scale_grid.addWidget(self.scale_square_max, 5, 3)
        return scale_grid

    def _create_rotation_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_button_ui(self):
        return QtWidgets.QVBoxLayout()

    def _create_connections(self):
        self.source_select_button.clicked.connect(self._get_current_select_single_object)
        self.destination_select_button.clicked.connect(self._get_current_select_multi_object_vertex)
        self.scale_square_checkbox.clicked.connect(self._toggle_scale_inputs)
        pass

    @QtCore.Slot()
    def _get_current_select_single_object(self):
        pass

    @QtCore.Slot()
    def _get_current_select_multi_object_vertex(self):
        pass

    @QtCore.Slot()
    def _toggle_scale_inputs(self):
        pass

    @QtCore.Slot()
    def _do_scatter(self):
        scatter = self._create_scatter_instance_from_fields()
        scatter.scatter_on_source(square_scale=self.square_tickbox.value())

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
