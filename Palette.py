import PySide2.QtGui as QtGui

class Palette(QtGui.QPalette):
    def __init__(self, windowText = None, button = None, light = None, dark = None, mid = None, text = None, bright_text = None, base = None, window = None):
        super(Palette, self).__init__()
        self.setBrush(QtGui.QPalette.WindowText, QtGui.QBrush(QtGui.QColor(255, 255, 255, 100)))    #Window titles and button titles?
        self.setBrush(QtGui.QPalette.ButtonText, QtGui.QBrush(QtGui.QColor(255, 255, 255, 150)))
        self.setBrush(QtGui.QPalette.Button, QtGui.QBrush(QtGui.QColor(25, 27, 29, 11)))
        self.setBrush(QtGui.QPalette.Light, QtGui.QBrush(QtGui.QColor(55, 50, 87, 70)))
        self.setBrush(QtGui.QPalette.Dark, QtGui.QBrush(QtGui.QColor(47, 58, 74, 29)))
        self.setBrush(QtGui.QPalette.Mid, QtGui.QBrush(QtGui.QColor(47, 58, 74, 55)))
        self.setBrush(QtGui.QPalette.Text, QtGui.QBrush(QtGui.QColor(255, 255, 255, 125)))
        self.setBrush(QtGui.QPalette.BrightText, QtGui.QBrush(QtGui.QColor(255, 255, 255, 100)))
        self.setBrush(QtGui.QPalette.Base, QtGui.QBrush(QtGui.QColor(25, 27, 29, 11)))
        self.setBrush(QtGui.QPalette.Window, QtGui.QBrush(QtGui.QColor(25, 27, 29, 11)))
        self.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtGui.QColor(255, 255, 255, 50)))
        self.setBrush(QtGui.QPalette.ToolTipBase, QtGui.QBrush(QtGui.QColor(25,27,29,20)))
        self.setBrush(QtGui.QPalette.ToolTipText, QtGui.QColor(QtGui.QColor(255,255,255,100)))