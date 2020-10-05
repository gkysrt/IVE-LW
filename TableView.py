import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import math
import Palette

class TableView(QtWidgets.QTableView):
    #Signal for middle button click
    mouseMiddleButtonClicked = QtCore.Signal(QtCore.QModelIndex, bool)
    listOrderChanged = QtCore.Signal(QtCore.QModelIndex, QtCore.QModelIndex)

    def __init__(self, parent = None):
        super(TableView, self).__init__(parent)
        #Set content details
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setShowGrid(False)
        self.setSortingEnabled(True)    #Makes list slower after the sorting
        self.setFrameStyle(self.NoFrame)
        self.setSelectionMode(self.SingleSelection)
        self.setDragDropMode(self.DragDrop)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.clickPos = None
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setAutoScroll(False)
        self.viewport().setAttribute(QtCore.Qt.WA_Hover)
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.setFocusPolicy(QtCore.Qt.NoFocus)
    #On left button click record click position
    def mousePressEvent(self, event):
        if (event.button() == QtCore.Qt.LeftButton):
            self.clickPos = event.pos()
        super(TableView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            #Calculate the distance between two points
            x1 = self.clickPos.x()
            y1 = self.clickPos.y()
            x2 = event.pos().x()
            y2 = event.pos().y()
            if(math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2)) > 10):
                self.startDrag(QtCore.Qt.MoveAction)

    def startDrag(self, dragAction):
        clickedItemIndex = self.indexAt(self.clickPos)

        if (clickedItemIndex.data() == None):
            return

        data = clickedItemIndex.siblingAtColumn(0).data(QtCore.Qt.UserRole).path()
        row = clickedItemIndex.row()

        #TODO: Enable and handle setRowHidden afterwards
        #self.setRowHidden(row, True)

        mimeData = QtCore.QMimeData()
        mimeData.setText(data)
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(QtGui.QPixmap(data).scaled(150,150,QtCore.Qt.KeepAspectRatio))
        drag.setHotSpot(QtCore.QPoint(drag.pixmap().width()/10*9, drag.pixmap().height()/10*9))

        #TODO: Add new features to drag operations?
        #parameter: QDropActions = MoveAction, CopyAction, LinkAction, ActionMask
        if(drag.exec_(QtCore.Qt.MoveAction) == QtCore.Qt.MoveAction):
            pass

    def dragEnterEvent(self, event):
        #Can add some actions or statements to drop action
        event.setDropAction(QtCore.Qt.MoveAction)
        event.acceptProposedAction()
       # print("asdsd")

    def dragMoveEvent(self, event):
        #Implement list items change position if drag hovers over items
        event.acceptProposedAction()

        #super(TableView, self).dragMoveEvent(event)

    def dropEvent(self, event):
       # print("asdsd")
        if(event.source() is self):
            #Item that is dragged
            draggedItemIndex = self.indexAt(self.clickPos)
            draggedRow = draggedItemIndex.row()

            #Item that is dropped on
            droppedItemIndex = self.indexAt(event.pos())
            droppedRow = droppedItemIndex.row()
            if ((draggedRow != droppedRow) and (droppedItemIndex.isValid())):
                self.listOrderChanged.emit(draggedItemIndex, droppedItemIndex)
            self.setCurrentIndex(self.indexAt(event.pos()))

        super(TableView, self).dropEvent(event)

    #Override mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        #If middle button is clicked emit mouseMiddleButtonClicked signal
        if (event.button() == QtCore.Qt.MouseButton.MiddleButton):
            self.mouseMiddleButtonClicked.emit(self.currentIndex(), False)

        if ((event.button() == QtCore.Qt.MouseButton.LeftButton) and (event.modifiers() & QtCore.Qt.ControlModifier)):
            self.mouseMiddleButtonClicked.emit(self.indexAt(event.pos()), True)
        super(TableView, self).mouseReleaseEvent(event)