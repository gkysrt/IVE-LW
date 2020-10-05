import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import math
import Palette

class ListView(QtWidgets.QListView):
    #Signal for middle button click
    mouseMiddleButtonClicked = QtCore.Signal(QtCore.QModelIndex, bool)
    listOrderChanged = QtCore.Signal(QtCore.QModelIndex, QtCore.QModelIndex)

    def __init__(self, parent = None):
        super(ListView, self).__init__(parent)
        #Set content details
        self.setFrameStyle(self.NoFrame)
        # self.setMaximumWidth(255)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.DragDrop)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.clickPos = None
        self.setMouseTracking(True)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setAutoScroll(True)
        self.setTextElideMode(QtCore.Qt.ElideRight)
        self.viewport().setAttribute(QtCore.Qt.WA_Hover)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)

    def keyPressEvent(self, event):
        if (event.key() == QtCore.Qt.Key_Escape):
            event.ignore()

        if (event.key() == QtCore.Qt.Key_Left):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_Right):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_Enter):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_W):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_Space):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_Q):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_S):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_F):
            event.ignore()

        elif (event.key() == QtCore.Qt.Key_Tab):
            event.ignore()

    #On left button click record click position
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.clickPos = event.pos()
        super(ListView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            #Calculate the distance between two points
            x1 = self.clickPos.x()
            y1 = self.clickPos.y()
            x2 = event.pos().x()
            y2 = event.pos().y()
            if(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)) > 10):
                self.initDrag()
        self.model().dataChanged.emit(self.indexAt(event.pos()), self.indexAt(event.pos()))

    def initDrag(self):
        clickedItemIndex = self.indexAt(self.clickPos)

        if (clickedItemIndex.data() == None):
            return

        data = clickedItemIndex.data()
        row = clickedItemIndex.row()

        #TODO: Enable and handle setRowHidden afterwards
        #self.setRowHidden(row, True)

        mimeData = QtCore.QMimeData()
        mimeData.setText(data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(QtGui.QPixmap(data).scaled(96,54,QtCore.Qt.KeepAspectRatio))
        drag.setHotSpot(QtCore.QPoint(drag.pixmap().width()/10*9, drag.pixmap().height()/10*9))

        #TODO: Add new features to drag operations?
        #parameter: QDropActions = MoveAction, CopyAction, LinkAction, ActionMask
        if(drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction):
            pass

    def dragEnterEvent(self, event):
        #Can add some actions or statements to drop action
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()

    def dragMoveEvent(self, event):
        #Implement list items change position if drag hovers over items
        if(event.source() is self):
            pass
        event.setDropAction(QtCore.Qt.MoveAction)
        event.accept()

    def dropEvent(self, event):
        if(event.source() is self):
            #Item that is dragged
            draggedItemIndex = self.indexAt(self.clickPos)
            draggedRow = draggedItemIndex.row()

            #Item that is dropped on
            droppedItemIndex = self.indexAt(event.pos())
            droppedRow = droppedItemIndex.row()
            #TODO: FIX CORE DUMP!!!!
            if (draggedRow + 1 == droppedRow):
                return
            if (draggedRow != droppedRow):
                self.listOrderChanged.emit(draggedItemIndex, droppedItemIndex)

        super(ListView, self).dropEvent(event)

    #Override mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        #If middle button is clicked emit mouseMiddleButtonClicked signal
        if (event.button() == QtCore.Qt.MouseButton.MiddleButton):
            self.mouseMiddleButtonClicked.emit(self.currentIndex(), False)

        if ((event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.modifiers() & QtCore.Qt.ControlModifier)):
            self.mouseMiddleButtonClicked.emit(self.indexAt(event.pos()), True)
        super(ListView, self).mouseReleaseEvent(event)
