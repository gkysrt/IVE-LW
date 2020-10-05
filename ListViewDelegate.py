import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
import os

class ListViewDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent = None):
        super(ListViewDelegate, self).__init__(parent)
        #Set a classwise brush and pen for items
        self.rect = QtCore.QRect(0, 0, 240, 60)
        self.titleFont = QtGui.QFont("Arial", 11, QtGui.QFont.Normal, False)
        self.titlePen = QtGui.QColor(149, 159, 250, 100)

        #Background variables
        self.backgroundColor = QtGui.QColor(47, 58, 74, 29)
        self.backgroundColor.setHsv(215, 37, 29)
        self.backgroundBrush = QtGui.QBrush()
        self.backgroundBrush.setColor(self.backgroundColor)
        self.backgroundBrush.setStyle(QtCore.Qt.SolidPattern)

        self.highlightBrush = QtGui.QBrush()
        self.highlightBrush.setColor(QtGui.QColor(255,255,255,50))
        self.highlightBrush.setStyle(QtCore.Qt.SolidPattern)

        self.hoveredBrush = QtGui.QBrush()
        self.hoveredBrush.setColor(QtGui.QColor(255,255,255,10))
        self.hoveredBrush.setStyle(QtCore.Qt.SolidPattern)

        self.detailColor = QtGui.QColor(255, 255, 255, 100)
        self.detailFont = QtGui.QFont("Arial", 8, QtGui.QFont.Light, True)

    #Parameters: QPainter painter, QStyleOptionViewItem option, QModelIndex index
    def paint(self, painter, option, index):
        painter.save()

        listViewSize = option.styleObject.size()
        painter.setBackground(self.backgroundBrush)
        painter.setPen(self.titlePen)
        painter.setFont(self.titleFont)
        painter.fillRect(option.rect, self.backgroundBrush)

        #If an item is selected highlight it and paint again
        if (option.state & QtWidgets.QStyle.State_Selected):
            painter.fillRect(option.rect, self.highlightBrush)

        if (option.state & QtWidgets.QStyle.State_MouseOver):
            painter.fillRect(option.rect, self.hoveredBrush)

        painter.drawText(QtCore.QRect(option.rect.x() + 5, option.rect.y() + 3, option.rect.width(), option.rect.height()/3), QtCore.Qt.AlignLeft, option.fontMetrics.elidedText(os.path.basename(index.data()), QtCore.Qt.ElideRight, listViewSize.width() - 10))
        painter.setFont(self.detailFont)
        painter.setPen(self.detailColor)
        painter.drawText(QtCore.QRect(option.rect.x() + 5, option.rect.y() + 23, option.rect.width(), option.rect.height()/4), QtCore.Qt.AlignLeft, option.fontMetrics.elidedText(os.path.dirname(index.data()), QtCore.Qt.ElideRight, listViewSize.width() - 10))
        painter.drawText(QtCore.QRect(option.rect.x() + 5, option.rect.y() + option.rect.height() - 15, option.rect.width()/3, option.rect.height()/4), QtCore.Qt.AlignLeft, option.fontMetrics.elidedText(index.data(QtCore.Qt.UserRole)[0] + "kB", QtCore.Qt.ElideRight, listViewSize.width()/3))
        painter.drawText(QtCore.QRect(option.rect.x() + (listViewSize.width()/2) +5, option.rect.y() + option.rect.height() - 15, (option.rect.width() * 2/3) - 5, option.rect.height()/4), QtCore.Qt.AlignLeft, option.fontMetrics.elidedText("Created: " + index.data(QtCore.Qt.UserRole)[1], QtCore.Qt.ElideRight, listViewSize.width() *2/3 - 20))

        painter.restore()

    #Parameters: QStyleOptionViewItem option, QModelIndex index
    #Returns: QSize
    def sizeHint(self, option, index):
        return self.rect.size()


