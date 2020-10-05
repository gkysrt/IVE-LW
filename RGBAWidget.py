import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore

import Palette

class RGBAWidget(QtWidgets.QTableWidget):
    def __init__(self, parent = None):
        super(RGBAWidget, self).__init__(parent)

        #Main setup of rgba widget
        #self.setPalette(Palette.Palette())
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setIconSize(QtCore.QSize(16, 16))
        self.setShowGrid(False)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setSelectionMode(QtWidgets.QTableWidget.SelectionMode.NoSelection)

        self.titleItem = QtWidgets.QTableWidgetItem()
        self.redItem = QtWidgets.QTableWidgetItem()
        self.greenItem = QtWidgets.QTableWidgetItem()
        self.blueItem = QtWidgets.QTableWidgetItem()
        self.pixelItem = QtWidgets.QTableWidgetItem()

        self.secondTitleItem = QtWidgets.QTableWidgetItem()
        self.secondRedItem = QtWidgets.QTableWidgetItem()
        self.secondGreenItem = QtWidgets.QTableWidgetItem()
        self.secondBlueItem = QtWidgets.QTableWidgetItem()
        self.secondPixelItem = QtWidgets.QTableWidgetItem()

        self.titleItem.setIcon(QtGui.QIcon("icons/image_detail"))
        self.redItem.setIcon(QtGui.QIcon("icons/red.svg"))
        self.greenItem.setIcon(QtGui.QIcon("icons/green.svg"))
        self.blueItem.setIcon(QtGui.QIcon("icons/blue.svg"))
        self.pixelItem.setIcon(QtGui.QIcon("icons/target_pixel.svg"))

        self.secondTitleItem.setIcon(QtGui.QIcon("icons/image_detail"))
        self.secondRedItem.setIcon(QtGui.QIcon("icons/red.svg"))
        self.secondGreenItem.setIcon(QtGui.QIcon("icons/green.svg"))
        self.secondBlueItem.setIcon(QtGui.QIcon("icons/blue.svg"))
        self.secondPixelItem.setIcon(QtGui.QIcon("icons/target_pixel.svg"))

        font = QtGui.QFont("Arial")
        font.setPointSize(10)
        titleFont = QtGui.QFont("Arial")
        titleFont.setBold(False)
        titleFont.setLetterSpacing(QtGui.QFont.PercentageSpacing, 100)

        self.titleItem.setFont(titleFont)
        self.pixelItem.setFont(font)
        self.redItem.setFont(font)
        self.greenItem.setFont(font)
        self.blueItem.setFont(font)

        self.secondTitleItem.setFont(titleFont)
        self.secondRedItem.setFont(font)
        self.secondGreenItem.setFont(font)
        self.secondBlueItem.setFont(font)
        self.secondPixelItem.setFont(font)

        self.titleItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.pixelItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.redItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.greenItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.blueItem.setTextAlignment(QtCore.Qt.AlignLeft)

        self.secondTitleItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.secondPixelItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.secondRedItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.secondGreenItem.setTextAlignment(QtCore.Qt.AlignLeft)
        self.secondBlueItem.setTextAlignment(QtCore.Qt.AlignLeft)

        self.titleItem.setText("Buffer ")
        self.redItem.setText("Red: \t")
        self.greenItem.setText("Green: \t")
        self.blueItem.setText("Blue: \t")
        self.pixelItem.setText("Pixel: \t")

        self.secondTitleItem.setText("Buffer S")
        self.secondRedItem.setText("Red:\t")
        self.secondGreenItem.setText("Green:\t")
        self.secondBlueItem.setText("Blue:\t")
        self.secondPixelItem.setText("Pixel:\t")

        self.setRowCount(5)
        self.setColumnCount(2)

        self.setItem(4, 0, self.blueItem)
        self.setItem(3, 0, self.greenItem)
        self.setItem(2, 0, self.redItem)
        self.setItem(1, 0, self.pixelItem)
        self.setItem(0, 0, self.titleItem)

        self.setItem(4, 1, self.secondBlueItem)
        self.setItem(3, 1, self.secondGreenItem)
        self.setItem(2, 1, self.secondRedItem)
        self.setItem(1, 1, self.secondPixelItem)
        self.setItem(0, 1, self.secondTitleItem)

        self.setColumnHidden(1, True)

        self.setColumnWidth(0, 170)
        self.setColumnWidth(1, 170)

        self.setRowHeight(0,20)
        self.setRowHeight(1,20)
        self.setRowHeight(2,20)
        self.setRowHeight(3,20)
        self.setRowHeight(4,20)

        self.verticalHeader().hide()
        self.horizontalHeader().hide()

    def setValues(self, title1, r1, g1, b1, a1, title2 = None, r2 = None, g2 = None, b2 = None, a2 = None):
        if((r2 is None) or (g2 is None) or (b2 is None) or (a2 is None)):
            self.setColumnHidden(1, True)
            self.titleItem.setText("Buffer " + title1 + "\t")
            self.redItem.setText("Red:\t" + str(r1))
            self.greenItem.setText("Green:\t" + str(g1))
            self.blueItem.setText("Blue:\t" + str(b1))
            self.pixelItem.setText("Pixel:\t" + str(a1))

        else:
            self.setColumnHidden(1, False)
            self.titleItem.setText("Buffer " + title1 + "\t")
            self.redItem.setText("Red:\t" + str(r1))
            self.greenItem.setText("Green:\t" + str(g1))
            self.blueItem.setText("Blue:\t" + str(b1))
            self.pixelItem.setText("Pixel:\t" + str(a1))

            self.secondTitleItem.setText("Buffer " + title2 + "\t")
            self.secondRedItem.setText("Red:\t" + str(r2))
            self.secondGreenItem.setText("Green:\t" + str(g2))
            self.secondBlueItem.setText("Blue:\t" + str(b2))
            self.secondPixelItem.setText("Pixel:\t" + str(a2))

        self.repaint()
