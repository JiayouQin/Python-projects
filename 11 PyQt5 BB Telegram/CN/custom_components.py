import sys
from PyQt5 import QtCore,QtWidgets

class CustomTextEdit(QtWidgets.QTextEdit):
    signal = QtCore.pyqtSignal(object)
    def __init__(self,parent=None):
        super(CustomTextEdit,self).__init__(parent)

