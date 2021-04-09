from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
import maya.cmds as cmds
from shiboken2 import wrapInstance
import logging
from scatter_instance import ScatterInstance

MIN_SCALE = 1.0
MIN_ROTATION = 0
MAX_ROTATION = 360

log = logging.getLogger(__name__)


def return_maya_main_window():
    main_window = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window), QtWidgets.QWidget)


class ScatterToolUI(QtWidgets.QDialog):
    def __init__(self):
        super(ScatterToolUI, self).__init__(parent=return_maya_main_window())
        self.setWindowTitle("Scatter Tool I")
        self.setMinimumWidth(500)
        self.setMinimumHeight(550)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.destination_holder = []
        self._create_ui()
        self._create_connections()

    def _create_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self.selection_layout = self._create_selection_ui()
        self.scale_layout = self._create_scale_ui()
        self.rotation_layout = self._create_rotation_ui()

        self.title_label = QtWidgets.QLabel("Scatter Tool")
        self.title_label.setStyleSheet("font: bold 20px;")

        self.scatter_button = QtWidgets.QPushButton("Scatter!")

        self.main_layout.addWidget(self.title_label)
        self.main_layout.addLayout(self.selection_layout)
        self.main_layout.addLayout(self.scale_layout)
        self.main_layout.addLayout(self.rotation_layout)
        self.main_layout.addStretch()
        self.main_layout.addWidget(self.scatter_button)

        self.setLayout(self.main_layout)

    def _create_selection_ui(self):
        self.source_label = QtWidgets.QLabel("Scatter Source")
        self.source_label.setStyleSheet("font: bold;")
        self.destination_label = QtWidgets.QLabel("Scatter Destination")
        self.destination_label.setStyleSheet("font: bold;")

        self.source_line_edit = QtWidgets.QLineEdit()
        self.source_line_edit.setMinimumWidth(150)
        self.source_line_edit.setDisabled(True)
        self.destination_text_box = QtWidgets.QTextEdit()
        self.destination_text_box.setMinimumWidth(150)
        self.destination_text_box.setMinimumHeight(50)
        self.destination_text_box.setMaximumHeight(50)
        self.destination_text_box.setDisabled(True)

        self.source_select_button = QtWidgets.QPushButton("Select")
        self.source_select_button.setMaximumWidth(75)
        self.destination_select_button = QtWidgets.QPushButton("Select")
        self.destination_select_button.setMaximumWidth(75)

        selection_layout = QtWidgets.QVBoxLayout()
        selection_layout.addWidget(self.source_label)

        selection_single_layout = QtWidgets.QHBoxLayout()
        selection_single_layout.addWidget(self.source_line_edit)
        selection_single_layout.addWidget(self.source_select_button)
        selection_single_layout.addStretch()
        selection_layout.addLayout(selection_single_layout)

        selection_layout.addWidget(self.destination_label)

        selection_multiple_layout = QtWidgets.QHBoxLayout()
        selection_multiple_layout.addWidget(self.destination_text_box)
        selection_multiple_layout.addWidget(self.destination_select_button)
        selection_multiple_layout.addStretch()
        selection_layout.addLayout(selection_multiple_layout)
        selection_layout.addSpacing(20)

        return selection_layout

    def _create_scale_ui(self):
        self.scale_label = QtWidgets.QLabel("Scale Ranges")
        self.scale_label.setStyleSheet("font: bold;")

        self.scale_x_label = QtWidgets.QLabel("X: ")
        self.scale_x_label.setStyleSheet("font: bold;")
        self.scale_y_label = QtWidgets.QLabel("Y: ")
        self.scale_y_label.setStyleSheet("font: bold;")
        self.scale_z_label = QtWidgets.QLabel("Z: ")
        self.scale_z_label.setStyleSheet("font: bold;")

        self.scale_square_label = QtWidgets.QLabel("Square Scale: ")
        self.scale_square_label.setStyleSheet("font: bold;")
        self.scale_xyz_label = QtWidgets.QLabel("XYZ: ")
        self.scale_xyz_label.setStyleSheet("font: bold;")

        self.scale_x_min = QtWidgets.QDoubleSpinBox()
        self.scale_x_min.setMinimumWidth(60)
        self.scale_x_min.setMinimum(MIN_SCALE)
        self.scale_x_max = QtWidgets.QDoubleSpinBox()
        self.scale_x_max.setMinimumWidth(60)
        self.scale_x_max.setMinimum(MIN_SCALE)

        self.scale_y_min = QtWidgets.QDoubleSpinBox()
        self.scale_y_min.setMinimumWidth(60)
        self.scale_y_min.setMinimum(MIN_SCALE)
        self.scale_y_max = QtWidgets.QDoubleSpinBox()
        self.scale_y_max.setMinimumWidth(60)
        self.scale_y_max.setMinimum(MIN_SCALE)

        self.scale_z_min = QtWidgets.QDoubleSpinBox()
        self.scale_z_min.setMinimumWidth(60)
        self.scale_z_min.setMinimum(MIN_SCALE)
        self.scale_z_max = QtWidgets.QDoubleSpinBox()
        self.scale_z_max.setMinimumWidth(60)
        self.scale_z_max.setMinimum(MIN_SCALE)

        self.scale_square_min = QtWidgets.QDoubleSpinBox()
        self.scale_square_min.setMinimumWidth(60)
        self.scale_square_min.setMinimum(MIN_SCALE)
        self.scale_square_min.setDisabled(True)
        self.scale_square_max = QtWidgets.QDoubleSpinBox()
        self.scale_square_max.setMinimumWidth(60)
        self.scale_square_max.setMinimum(MIN_SCALE)
        self.scale_square_max.setDisabled(True)

        self.scale_square_checkbox = QtWidgets.QCheckBox()

        scale_layout = QtWidgets.QVBoxLayout()
        scale_layout.addWidget(self.scale_label)

        scale_x_layout = QtWidgets.QHBoxLayout()
        scale_x_layout.addWidget(self.scale_x_label)
        scale_x_layout.addWidget(self.scale_x_min)
        scale_x_layout.addWidget(QtWidgets.QLabel("-"))
        scale_x_layout.addWidget(self.scale_x_max)
        scale_x_layout.addStretch()
        scale_layout.addLayout(scale_x_layout)

        scale_y_layout = QtWidgets.QHBoxLayout()
        scale_y_layout.addWidget(self.scale_y_label)
        scale_y_layout.addWidget(self.scale_y_min)
        scale_y_layout.addWidget(QtWidgets.QLabel("-"))
        scale_y_layout.addWidget(self.scale_y_max)
        scale_y_layout.addStretch()
        scale_layout.addLayout(scale_y_layout)

        scale_z_layout = QtWidgets.QHBoxLayout()
        scale_z_layout.addWidget(self.scale_z_label)
        scale_z_layout.addWidget(self.scale_z_min)
        scale_z_layout.addWidget(QtWidgets.QLabel("-"))
        scale_z_layout.addWidget(self.scale_z_max)
        scale_z_layout.addStretch()
        scale_layout.addLayout(scale_z_layout)
        scale_layout.addSpacing(10)

        scale_check_layout = QtWidgets.QHBoxLayout()
        scale_check_layout.addWidget(self.scale_square_label)
        scale_check_layout.addWidget(self.scale_square_checkbox)
        scale_check_layout.addStretch()
        scale_layout.addLayout(scale_check_layout)

        scale_square_layout = QtWidgets.QHBoxLayout()
        scale_square_layout.addWidget(self.scale_xyz_label)
        scale_square_layout.addWidget(self.scale_square_min)
        scale_square_layout.addWidget(QtWidgets.QLabel("-"))
        scale_square_layout.addWidget(self.scale_square_max)
        scale_square_layout.addStretch()
        scale_layout.addLayout(scale_square_layout)
        scale_layout.addSpacing(20)

        return scale_layout

    def _create_rotation_ui(self):
        self.rotation_label = QtWidgets.QLabel("Rotation Ranges")
        self.rotation_label.setStyleSheet("font: bold;")

        self.rotation_x_label = QtWidgets.QLabel("X: ")
        self.rotation_x_label.setStyleSheet("font: bold;")
        self.rotation_y_label = QtWidgets.QLabel("Y: ")
        self.rotation_y_label.setStyleSheet("font: bold;")
        self.rotation_z_label = QtWidgets.QLabel("Z: ")
        self.rotation_z_label.setStyleSheet("font: bold;")

        self.rotation_x_min = QtWidgets.QDoubleSpinBox()
        self.rotation_x_min.setMinimumWidth(60)
        self.rotation_x_min.setRange(MIN_ROTATION, 360)
        self.rotation_x_max = QtWidgets.QDoubleSpinBox()
        self.rotation_x_max.setMinimumWidth(60)
        self.rotation_x_max.setRange(MIN_ROTATION, 360)

        self.rotation_y_min = QtWidgets.QDoubleSpinBox()
        self.rotation_y_min.setMinimumWidth(60)
        self.rotation_y_min.setRange(MIN_ROTATION, 360)
        self.rotation_y_max = QtWidgets.QDoubleSpinBox()
        self.rotation_y_max.setMinimumWidth(60)
        self.rotation_y_max.setRange(MIN_ROTATION, 360)

        self.rotation_z_min = QtWidgets.QDoubleSpinBox()
        self.rotation_z_min.setMinimumWidth(60)
        self.rotation_z_min.setRange(MIN_ROTATION, 360)
        self.rotation_z_max = QtWidgets.QDoubleSpinBox()
        self.rotation_z_max.setMinimumWidth(60)
        self.rotation_z_max.setRange(MIN_ROTATION, 360)

        rotation_layout = QtWidgets.QVBoxLayout()
        rotation_layout.addWidget(self.rotation_label)

        rotation_x_layout = QtWidgets.QHBoxLayout()
        rotation_x_layout.addWidget(self.rotation_x_label)
        rotation_x_layout.addWidget(self.rotation_x_min)
        rotation_x_layout.addWidget(QtWidgets.QLabel("-"))
        rotation_x_layout.addWidget(self.rotation_x_max)
        rotation_x_layout.addStretch()
        rotation_layout.addLayout(rotation_x_layout)

        rotation_y_layout = QtWidgets.QHBoxLayout()
        rotation_y_layout.addWidget(self.rotation_y_label)
        rotation_y_layout.addWidget(self.rotation_y_min)
        rotation_y_layout.addWidget(QtWidgets.QLabel("-"))
        rotation_y_layout.addWidget(self.rotation_y_max)
        rotation_y_layout.addStretch()
        rotation_layout.addLayout(rotation_y_layout)

        rotation_z_layout = QtWidgets.QHBoxLayout()
        rotation_z_layout.addWidget(self.rotation_z_label)
        rotation_z_layout.addWidget(self.rotation_z_min)
        rotation_z_layout.addWidget(QtWidgets.QLabel("-"))
        rotation_z_layout.addWidget(self.rotation_z_max)
        rotation_z_layout.addStretch()
        rotation_layout.addLayout(rotation_z_layout)

        return rotation_layout

    def _create_connections(self):
        self.source_select_button.clicked.connect(self._get_current_select_single_object)
        self.destination_select_button.clicked.connect(self._get_current_select_multi_object_vertex)
        self.scale_square_checkbox.clicked.connect(self._toggle_scale_inputs)
        self.scatter_button.clicked.connect(self._do_scatter)

    @QtCore.Slot()
    def _get_current_select_single_object(self):
        full_selection = cmds.ls(selection=True)
        if len(full_selection) > 1:
            log.warning("Only the first selection will be used for the source.")

        single_selection = ""
        try:
            single_selection = full_selection[0]
        except IndexError:
            log.warning("You have nothing selected or do not have a valid object selected!")

        if single_selection:
            self.source_line_edit.setText(single_selection)

    @QtCore.Slot()
    def _get_current_select_multi_object_vertex(self):
        full_selection = cmds.ls(selection=True, flatten=True)
        self.destination_text_box.setText(','.join(full_selection))
        object_references = []
        vertex_references = []
        for selection in full_selection:
            encoded_selection = selection.encode("utf-8")
            if ".vtx" in encoded_selection:
                vertex_references.append(selection)
            else:
                object_references.append(selection)

        if object_references:
            vertex_ranges = cmds.polyListComponentConversion(object_references, toVertex=True)
            vertex_references.extend(cmds.filterExpand(vertex_ranges, selectionMask=31))

        self.destination_holder = vertex_references

    @QtCore.Slot()
    def _toggle_scale_inputs(self):
        # flip flops between enabled and disabled
        self.scale_x_min.setDisabled(self.scale_x_min.isEnabled())
        self.scale_x_max.setDisabled(self.scale_x_max.isEnabled())
        self.scale_y_min.setDisabled(self.scale_y_min.isEnabled())
        self.scale_y_max.setDisabled(self.scale_y_max.isEnabled())
        self.scale_z_min.setDisabled(self.scale_z_min.isEnabled())
        self.scale_z_max.setDisabled(self.scale_z_max.isEnabled())
        self.scale_square_min.setDisabled(self.scale_square_min.isEnabled())
        self.scale_square_max.setDisabled(self.scale_square_max.isEnabled())

    @QtCore.Slot()
    def _do_scatter(self):
        scatter = self._create_scatter_instance_from_fields()
        scatter.scatter_on_source(square_scale=self.scale_square_checkbox.isChecked())

    def _create_scatter_instance_from_fields(self):
        scale_ranges = self._get_scale_ranges()
        rotation_ranges = self._get_rotation_ranges()
        source_object = str(self.source_line_edit.text())
        destinations = self.destination_holder
        return ScatterInstance(source_object, destinations,
                               scale_ranges, rotation_ranges)

    def _get_scale_ranges(self):
        if self.scale_square_checkbox.isChecked():
            scale_range = (float(self.scale_square_min.value()), float(self.scale_square_max.value()))
            return scale_range, scale_range, scale_range
        scale_x_range = (float(self.scale_x_min.value()), float(self.scale_x_max.value()))
        scale_y_range = (float(self.scale_y_min.value()), float(self.scale_y_max.value()))
        scale_z_range = (float(self.scale_z_min.value()), float(self.scale_z_max.value()))
        return scale_x_range, scale_y_range, scale_z_range

    def _get_rotation_ranges(self):
        rotation_x_range = (float(self.rotation_x_min.value()), float(self.rotation_x_max.value()))
        rotation_y_range = (float(self.rotation_y_min.value()), float(self.rotation_y_max.value()))
        rotation_z_range = (float(self.rotation_z_min.value()), float(self.rotation_z_max.value()))
        return rotation_x_range, rotation_y_range, rotation_z_range
