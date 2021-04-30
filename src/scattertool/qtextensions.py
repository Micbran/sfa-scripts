from PySide2 import QtWidgets


class PaddedQSpinBox(QtWidgets.QSpinBox):
    def __init__(self, padding=3, parent=None, *args):
        super(PaddedQSpinBox, self).__init__(parent)
        self.padding = padding

    def textFromValue(self, value):
        return "%0*d" % (self.padding, value)


class PercentQDoubleSpinBox(QtWidgets.QDoubleSpinBox):
    def __init__(self, parent=None, *args):
        super(PercentQDoubleSpinBox, self).__init__(parent)

    def textFromValue(self, value):
        return "%10.2f%s" % (value, '%')
