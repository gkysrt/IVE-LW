import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import PySide2.QtWidgets as QtWidgets
import os


class TableViewDelegate(QtWidgets.QStyledItemDelegate):

    def __init__(self, parent=None):
        super(TableViewDelegate, self).__init__(parent)
        # Set a classwise brush and pen for items
        self.titleColumnRect = QtCore.QRect(0, 0, 180, 30)
        self.sizeColumnRect = QtCore.QRect(0, 0, 70, 30)
        self.dateColumnRect = QtCore.QRect(0, 0, 90, 30)
        self.tagsColumnRect = QtCore.QRect(0, 0, 90, 30)
        self.directoryColumnRect = QtCore.QRect(0, 0, 120, 30)
        self.resolutionColumnRect = QtCore.QRect(0, 0, 90, 30)

        self.titleFont = QtGui.QFont("Arial", 9, QtGui.QFont.Normal, False)
        self.selectedPen = QtGui.QColor(225, 150, 0, 255)

        # Background variables
        self.backgroundColor = QtGui.QColor(64, 64, 64, 255)
        self.backgroundBrush = QtGui.QBrush()
        self.backgroundBrush.setColor(self.backgroundColor)
        self.backgroundBrush.setStyle(QtCore.Qt.SolidPattern)

        self.highlightBrush = QtGui.QBrush()
        self.highlightBrush.setColor(QtGui.QColor(255, 255, 255, 50))
        self.highlightBrush.setStyle(QtCore.Qt.SolidPattern)

        self.hoveredBrush = QtGui.QBrush()
        self.hoveredBrush.setColor(QtGui.QColor(255, 255, 255, 10))
        self.hoveredBrush.setStyle(QtCore.Qt.SolidPattern)

        self.detailColor = QtGui.QColor(255, 255, 255, 100)
        self.detailFont = QtGui.QFont("Arial", 8, QtGui.QFont.Light, True)

    # Parameters: QPainter painter, QStyleOptionViewItem option, QModelIndex index
    def paint(self, painter, option, index):
        painter.save()
        column = index.column()
        tableViewSize = option.styleObject.size()
        painter.setBackground(self.backgroundBrush)
        painter.setFont(self.titleFont)
        painter.fillRect(option.rect, self.backgroundBrush)
        fontMetric = painter.fontMetrics()

        # If an item is selected highlight it and paint again
        if option.state & QtWidgets.QStyle.State_Selected:
            painter.fillRect(option.rect, self.highlightBrush)
            painter.setPen(self.selectedPen)

        if option.state & QtWidgets.QStyle.State_MouseOver:
            painter.fillRect(option.rect, self.hoveredBrush)

        if column == 0:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(os.path.basename(index.data()), QtCore.Qt.ElideRight,
                                                   option.rect.width()))

        elif column == 1:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(self.fileSizeString(index.data()), QtCore.Qt.ElideRight,
                                                   option.rect.width()))

        elif column == 2:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(str(index.data()), QtCore.Qt.ElideRight, option.rect.width()))

        elif column == 3:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(str(index.data()), QtCore.Qt.ElideRight, option.rect.width()))

        elif column == 4:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(str(index.data()), QtCore.Qt.ElideRight, option.rect.width()))

        elif column == 5:
            painter.drawText(option.rect, QtCore.Qt.AlignCenter,
                             fontMetric.elidedText(str(index.data()), QtCore.Qt.ElideRight, option.rect.width()))

        painter.restore()

    # Parameters: QStyleOptionViewItem option, QModelIndex index
    # Returns: QSize
    def sizeHint(self, option, index):
        if index.column() == 0:
            return self.titleColumnRect.size()

        elif index.column() == 1:
            return self.sizeColumnRect.size()

        elif index.column() == 2:
            return self.dateColumnRect.size()

        elif index.column() == 3:
            return self.resolutionColumnRect.size()

        elif index.column() == 4:
            return self.directoryColumnRect.size()

        elif index.column() == 5:
            return self.tagsColumnRect.size()

    # Returns a string for display according to the given size
    def fileSizeString(self, size):
        size = int(size)
        # Normally size are multiplied with 1024 but ubuntu multiplies with 1000
        if size / 1000000 < 1:
            return str(size / 1000)[:5] + " kB"

        elif size / 1000000000 < 1:
            return str(size / 1000000)[:4] + " MB"

        else:
            return (str(size / 1000000000))[:4] + " GB"
