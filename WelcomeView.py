import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import os

class WelcomeView(QtWidgets.QGraphicsView):
    newFolderClicked = QtCore.Signal()
    newFileClicked = QtCore.Signal()
    loadListClicked = QtCore.Signal()
    lastSessionClicked = QtCore.Signal()
    recentPathsClicked = QtCore.Signal(str)

    def __init__(self, parent = None):
        super(WelcomeView, self).__init__(parent)
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.setAcceptDrops(False)

        self.backgroundColor = QtGui.QColor(30, 30, 30, 255)
        self.backgroundBrush = QtGui.QBrush()
        self.backgroundBrush.setColor(self.backgroundColor)
        self.backgroundBrush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(self.backgroundBrush)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)

        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.sceneRectangle = QtCore.QRect(0,0,640,360)
        self.setSceneRect(self.sceneRectangle)

        self.titleFont = QtGui.QFont()
        self.titleFont.setPointSize(150)
        self.titleFont.setFamily("Arial")

        self.titleText = QtWidgets.QGraphicsTextItem("IVE")
        self.titleText.setFont(self.titleFont)
        self.titleText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.titleText.setPos(self.sceneRect().width()/2 - self.titleText.sceneBoundingRect().width()/2, 0)
        #self.titleText.setPos(self.sceneRect().center().x() - self.titleText.boundingRect().center().x(), 0)
        
        self.secondaryTitleFont = QtGui.QFont()
        self.secondaryTitleFont.setPointSize(15)
        self.secondaryTitleFont.setFamily("Arial")
        self.secondaryTitleFont.setBold(False)

        self.startText = QtWidgets.QGraphicsTextItem("Start")
        self.startText.setFont(self.secondaryTitleFont)
        self.startText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.startText.setPos(self.titleText.x(), self.titleText.boundingRect().height())

        self.subTextFont = QtGui.QFont()
        self.subTextFont.setPointSize(10)
        self.subTextFont.setFamily("Arial")

        self.newFolderSubText = QtWidgets.QGraphicsTextItem("Open Folder")
        self.newFolderSubText.setFont(self.subTextFont)
        self.newFolderSubText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.newFolderSubText.setPos(self.titleText.x(), self.startText.scenePos().y() + 40)
        self.newFolderSubText.setCursor(QtCore.Qt.PointingHandCursor)

        self.newFolderShortcutText = QtWidgets.QGraphicsTextItem("Ctrl+O")
        self.newFolderShortcutText.setFont(self.subTextFont)
        self.newFolderShortcutText.setDefaultTextColor(QtGui.QColor(255,255,255,100))
        self.newFolderShortcutText.setPos(self.newFolderSubText.sceneBoundingRect().x() + 120, self.startText.scenePos().y() + 40)

        self.newFileSubText = QtWidgets.QGraphicsTextItem("New File")
        self.newFileSubText.setFont(self.subTextFont)
        self.newFileSubText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.newFileSubText.setPos(self.titleText.x(), self.newFolderSubText.scenePos().y() + 25)
        self.newFileSubText.setCursor(QtCore.Qt.PointingHandCursor)

        self.newFileShortcutText = QtWidgets.QGraphicsTextItem("Ctrl+I")
        self.newFileShortcutText.setFont(self.subTextFont)
        self.newFileShortcutText.setDefaultTextColor(QtGui.QColor(255,255,255,100))
        self.newFileShortcutText.setPos(self.newFileSubText.sceneBoundingRect().x() + 120, self.newFolderSubText.scenePos().y() + 25)

        self.loadListSubText = QtWidgets.QGraphicsTextItem("Load List")
        self.loadListSubText.setFont(self.subTextFont)
        self.loadListSubText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.loadListSubText.setPos(self.titleText.x(), self.newFileSubText.scenePos().y() + 25)
        self.loadListSubText.setCursor(QtCore.Qt.PointingHandCursor)

        self.loadListShortcutText = QtWidgets.QGraphicsTextItem("Ctrl+L")
        self.loadListShortcutText.setFont(self.subTextFont)
        self.loadListShortcutText.setDefaultTextColor(QtGui.QColor(255,255,255,100))
        self.loadListShortcutText.setPos(self.loadListSubText.sceneBoundingRect().x() + 120, self.newFileSubText.scenePos().y() + 25)

        self.openRecentSubText = QtWidgets.QGraphicsTextItem("Open Last Session")
        self.openRecentSubText.setFont(self.subTextFont)
        self.openRecentSubText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.openRecentSubText.setPos(self.titleText.x(), self.loadListSubText.scenePos().y() + 25)
        self.openRecentSubText.setCursor(QtCore.Qt.PointingHandCursor)

        self.openRecentShortcutText = QtWidgets.QGraphicsTextItem("Ctrl+R")
        self.openRecentShortcutText.setFont(self.subTextFont)
        self.openRecentShortcutText.setDefaultTextColor(QtGui.QColor(255,255,255,100))
        self.openRecentShortcutText.setPos(self.openRecentSubText.sceneBoundingRect().x() + 120, self.loadListSubText.scenePos().y() + 25)

        self.recentText = QtWidgets.QGraphicsTextItem("Recent")
        self.recentText.setFont(self.secondaryTitleFont)
        self.recentText.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.recentText.setPos(self.sceneRect().width()*3/5, self.titleText.boundingRect().height())

        self.firstRecent = QtWidgets.QGraphicsTextItem()
        self.firstRecent.setFont(self.subTextFont)
        self.firstRecent.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.firstRecent.setPos(self.recentText.x(), self.recentText.scenePos().y() + 40)
        self.firstRecent.setCursor(QtCore.Qt.PointingHandCursor)
        self.firstRecent.hide()

        self.secondRecent = QtWidgets.QGraphicsTextItem()
        self.secondRecent.setFont(self.subTextFont)
        self.secondRecent.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.secondRecent.setPos(self.recentText.x(), self.firstRecent.scenePos().y() + 25)
        self.secondRecent.setCursor(QtCore.Qt.PointingHandCursor)
        self.secondRecent.hide()

        self.thirdRecent = QtWidgets.QGraphicsTextItem()
        self.thirdRecent.setFont(self.subTextFont)
        self.thirdRecent.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.thirdRecent.setPos(self.recentText.x(), self.secondRecent.scenePos().y() + 25)
        self.thirdRecent.setCursor(QtCore.Qt.PointingHandCursor)
        self.thirdRecent.hide()

        self.fourthRecent = QtWidgets.QGraphicsTextItem()
        self.fourthRecent.setFont(self.subTextFont)
        self.fourthRecent.setDefaultTextColor(QtGui.QColor(255,255,255,175))
        self.fourthRecent.setPos(self.recentText.x(), self.thirdRecent.scenePos().y() + 25)
        self.fourthRecent.setCursor(QtCore.Qt.PointingHandCursor)
        self.fourthRecent.hide()

        self.scene.addItem(self.titleText)
        self.scene.addItem(self.startText)
        self.scene.addItem(self.newFolderSubText)
        self.scene.addItem(self.newFileSubText)
        self.scene.addItem(self.loadListSubText)
        self.scene.addItem(self.openRecentSubText)
        self.scene.addItem(self.newFolderShortcutText)
        self.scene.addItem(self.newFileShortcutText)
        self.scene.addItem(self.loadListShortcutText)
        self.scene.addItem(self.openRecentShortcutText)
        self.scene.addItem(self.recentText)
        self.scene.addItem(self.firstRecent)
        self.scene.addItem(self.secondRecent)
        self.scene.addItem(self.thirdRecent)
        self.scene.addItem(self.fourthRecent)

        self.newFolderMousePress = False
        self.newFileMousePress = False
        self.loadListMousePress = False
        self.openRecentMousePress = False
        self.firstRecentMousePress = False
        self.secondRecentMousePress = False
        self.thirdRecentMousePress = False
        self.fourthRecentMousePress = False

    def resizeEvent(self, event):
        self.ensureVisible(self.sceneRectangle)
        self.centerOn(self.scene.itemsBoundingRect().center())

        super().resizeEvent(event)

    def mousePressEvent(self, event):
        if(event.button() is QtCore.Qt.LeftButton):
            if(self.newFolderSubText.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.newFolderMousePress = True

            elif(self.newFileSubText.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.newFileMousePress = True

            elif(self.loadListSubText.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.loadListMousePress = True

            elif(self.openRecentSubText.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.openRecentMousePress = True

            elif(self.firstRecent.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.firstRecentMousePress = True
        
            elif(self.secondRecent.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.secondRecentMousePress = True
        
            elif(self.thirdRecent.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.thirdRecentMousePress = True
        
            elif(self.fourthRecent.sceneBoundingRect().contains(self.mapToScene(event.pos()))):
                self.fourthRecentMousePress = True

        super().mousePressEvent(event)

    def mouseReleaseEvent(self,event):
        if(event.button() is QtCore.Qt.LeftButton):

            if(self.newFolderSubText.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.newFolderMousePress):
                self.newFolderClicked.emit()
            
            elif(self.newFileSubText.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.newFileMousePress):
                self.newFileClicked.emit()
            
            elif(self.loadListSubText.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.loadListMousePress):
                self.loadListClicked.emit()
            
            elif(self.openRecentSubText.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.openRecentMousePress):
                self.lastSessionClicked.emit()
            
            elif(self.firstRecent.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.firstRecentMousePress):
                self.recentPathsClicked.emit(os.path.realpath(self.firstRecent.toPlainText()))
            
            elif(self.secondRecent.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.secondRecentMousePress):
                self.recentPathsClicked.emit(os.path.realpath(self.secondRecent.toPlainText()))

            elif(self.thirdRecent.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.thirdRecentMousePress):
                self.recentPathsClicked.emit(os.path.realpath(self.thirdRecent.toPlainText()))

            elif(self.fourthRecent.sceneBoundingRect().contains(self.mapToScene(event.pos())) and self.fourthRecentMousePress):
                self.recentPathsClicked.emit(os.path.realpath(self.fourthRecent.toPlainText()))

        self.openRecentMousePress = False
        self.newFolderMousePress = False
        self.newFileMousePress = False
        self.loadListMousePress = False
        self.firstRecentMousePress = False
        self.secondRecentMousePress = False
        self.thirdRecentMousePress = False
        self.fourthRecentMousePress = False

        super().mouseReleaseEvent(event)

    def deleteLater(self):
        #Add some details maybe?
        super().deleteLater()
    
    def keyPressEvent(self, event):
        if(event.key() == QtCore.Qt.Key_Left):
            event.ignore()

        elif(event.key() == QtCore.Qt.Key_Right):
            event.ignore()
        else:
            return super().keyPressEvent(event)

    #To disable scrolling with wheel
    def wheelEvent(self, event):
        return

    def setRecentDirectories(self, dirList):
        copyList = dirList.copy()
        try:
            self.firstRecent.setPlainText(os.path.relpath(copyList.pop()))
            self.firstRecent.show()
            self.secondRecent.setPlainText(os.path.relpath(copyList.pop()))
            self.secondRecent.show()
            self.thirdRecent.setPlainText(os.path.relpath(copyList.pop()))
            self.thirdRecent.show()
            self.fourthRecent.setPlainText(os.path.relpath(copyList.pop()))
            self.fourthRecent.show()
        except:
            pass
