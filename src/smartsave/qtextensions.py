from PySide2 import QtWidgets


class PaddedQSpinBox(QtWidgets.QSpinBox):
	def __init__(self, padding=3, parent=None, *args):
		super(PaddedQSpinBox, self).__init__(parent)
		self.padding = padding

	def textFromValue(self, value):
		return "%0*d" % (self.padding, value)
