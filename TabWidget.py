import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import ImageView
import WelcomeView
import os
import TabBarWidget

class TabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent = None):
        super(TabWidget, self).__init__(parent)

        self.setTabShape(self.TabShape.Rounded)
        self.setTabPosition(self.TabPosition.North)
        self.setElideMode(QtCore.Qt.ElideRight)
        self.setTabsClosable(True)
        self.setUsesScrollButtons(True)
        self.setMovable(True)   #Set QTabWidget preferences
        self.setElideMode(QtCore.Qt.ElideRight) #Set QTabWidget preferences
        self.tabCloseRequested.connect(self.closeTab)   #Connect tab close signal
        self.middleClickedTabIndex = 0  #Track which tab is middleclicked
        self.welcomePage = WelcomeView.WelcomeView(self)
        self.openWelcomeTab()

        self.mainStatusBar = QtWidgets.QFrame(parent)
        self.mainStatusBarLayout = QtWidgets.QHBoxLayout(self.mainStatusBar)
        self.mainStatusBarLayout.setSpacing(0)
        self.mainStatusBar.setFixedHeight(20)
        self.mainStatusBarLayout.setContentsMargins(0, 0, 0, 0)
        self.mainStatusBarLayout.setMargin(0)
        #self.mainStatusBar.setStyleSheet("border:1px solid red")
        self.statusSpacer = QtWidgets.QWidget(self.mainStatusBar)
        self.statusSpacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.zoomInButton = QtWidgets.QPushButton(self.mainStatusBar)
        self.zoomInButton.setIcon(QtGui.QIcon("icons/zoom_in.svg"))
        self.zoomButton = QtWidgets.QPushButton("%100",self.mainStatusBar)
        self.zoomOutButton = QtWidgets.QPushButton(self.mainStatusBar)
        self.zoomOutButton.setIcon(QtGui.QIcon("icons/zoom_out.svg"))

        self.zoomInButton.setFixedWidth(20)
        self.zoomButton.setFixedWidth(60)
        self.zoomOutButton.setFixedWidth(20)
        self.zoomButton.setStyleSheet("QPushButton {margin:0px; border: 3px solid rgb(50,50,50); background-color: rgb(50,50,50); border-radius: 3px; font-family:'Arial'; font-size: 10pt; color:rgba(255, 255, 255, 100);} QPushButton:pressed {border: 3px solid #252629; background-color: #252629;} QPushButton:hover:!pressed {border: 3px solid #2E3033; background-color: #2E3033;}")
        self.zoomInButton.setStyleSheet("QPushButton {margin:0px; border: 3px solid #585A5B; background-color: #585A5B; border-radius: 3px;} QPushButton:pressed {border: 3px solid #5E6069; background-color: #5E6069;} QPushButton:hover:!pressed {border: 3px solid #676C73; background-color: #676C73;}")
        self.zoomOutButton.setStyleSheet("QPushButton {margin:0px; border: 3px solid #585A5B; background-color: #585A5B; border-radius: 3px;} QPushButton:pressed {border: 3px solid #5E6069; background-color: #5E6069;} QPushButton:hover:!pressed {border: 3px solid #676C73; background-color: #676C73;}")

        self.zoomInButton.clicked.connect(self.zoomIn)
        self.zoomButton.clicked.connect(self.resetZoom)
        self.zoomOutButton.clicked.connect(self.zoomOut)

        self.mainStatusBarLayout.addWidget(self.statusSpacer)
        self.mainStatusBarLayout.addWidget(self.zoomOutButton)
        self.mainStatusBarLayout.addWidget(self.zoomButton)
        self.mainStatusBarLayout.addWidget(self.zoomInButton)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

    def closeTab(self, index = None):
        self.widget(index).deleteLater()    #Delete page inside the tab
        self.removeTab(index)
        if(self.count() == 0):
            self.addNewTab()

    # For basic opening image operations. If no tabs present, opens a new tab and the image with the given index.
    # Otherwise, opens image with the given index in current tab.
    def openImage(self, index):
        filePath = index.siblingAtColumn(0).data(QtCore.Qt.UserRole).path()
        fileIndex = index.row()
        if self.count() == 0 or self.currentWidget() is self.welcomePage:
            newImage = ImageView.ImageView(self)
            newImage.loadImage(filePath)
            newImage.bufferPixmapChanged.connect(self.updateContent)
            newImage.imageZoomChanged.connect(self.updateZoom)
            newTabIndex = self.insertTab(self.count(), newImage, os.path.basename(filePath))
            self.setTabToolTip(newTabIndex, os.path.basename(filePath))
            self.setCurrentWidget(self.widget(newTabIndex))
            newImage.fitImage()
        else:
            self.currentWidget().loadImage(filePath)
            self.setTabToolTip(self.currentIndex(), os.path.basename(filePath))


    #Adds a new empty tab
    def addNewTab(self):
        emptyView = ImageView.ImageView(self)
        emptyView.bufferPixmapChanged.connect(self.updateContent)
        emptyView.imageZoomChanged.connect(self.updateZoom)
        newTabIndex = self.addTab(emptyView, "New Tab")
        self.setCurrentWidget(self.widget(newTabIndex))

    #When listView is clicked with middle mouse button this function is triggered.
    #Opens an image in a new tab
    def openNewImageTab(self, index, showTab = False):
        filePath = index.siblingAtColumn(0).data(QtCore.Qt.UserRole).path()
        fileIndex = index.row()

        newImage = ImageView.ImageView(self)
        newImage.loadImage(filePath)
        newImage.bufferPixmapChanged.connect(self.updateContent)
        newImage.imageZoomChanged.connect(self.updateZoom)
        newTabIndex = self.insertTab(self.count(), newImage, os.path.basename(filePath))
        self.setTabToolTip(newTabIndex, os.path.basename(filePath))

        if(showTab):
            self.setCurrentWidget(self.widget(newTabIndex))

    def openWelcomeTab(self):
        newTabIndex = self.insertTab(self.count(), self.welcomePage, "Welcome")


    def updateContent(self, fileName):
        self.setTabText(self.currentIndex(), os.path.basename(fileName))

    def updateZoom(self, zoom):
        self.zoomButton.setText(str(zoom) + "%")

    def zoomIn(self):
        try:
            self.currentWidget().zoom(1.3)
        except AttributeError:
            pass

    def zoomOut(self):
        try:
            self.currentWidget().zoom(10/13)
        except AttributeError:
            pass

    def resetZoom(self):
        try:
            self.currentWidget().zoom()
        except AttributeError:
            pass

    def mousePressEvent(self, event):
        self.middleClickedTabIndex = self.tabBar().tabAt(event.pos())
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if(event.button() == QtCore.Qt.MiddleButton):
            if(self.middleClickedTabIndex == self.tabBar().tabAt(event.pos())):
                self.closeTab(self.tabBar().tabAt(event.pos()))
        super().mouseReleaseEvent(event)