import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import DataModel
import DataAccess
import DataAdapter
import ProxyModel
import TabWidget
import DockWidget
import Palette


class Display(QtWidgets.QMainWindow):
    def __init__(self, screens, parent=None):
        super(Display, self).__init__(parent)
        with open("themes/Ive.qss", "r") as qssFile:
            style = qssFile.read()

        qssFile.closed
        self.setStyleSheet(style)
        generalPalette = Palette.Palette()
        # self.setPalette(generalPalette)
        # Get screen size of the computer and open QMainWindow according to constraints below
        screenSize = screens[0].size()
        # self.setMinimumSize(screenSize.width()/2,screenSize.height()/2)
        self.move(screenSize.width() / 4, screenSize.height() / 4)

        # Instantiate mainLayout, mainWidget and add set mainLayout for mainWidget
        self.mainWidget = QtWidgets.QWidget()
        self.mainLayout = QtWidgets.QVBoxLayout(self.mainWidget)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.mainLayout.setSpacing(0)

        self.setCentralWidget(self.mainWidget)
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint)

        # Instantiate DataModel and set data
        self.dataThread = QtCore.QThread(self)
        self.dataThread.setObjectName("Adapter Thread")
        self.dataAccess = DataAccess.DataAccess()  # Data access returns image list as string list
        self.dataAccess.saveList.connect(self.dataAccess._saveList)
        self.dataAccess.scan.connect(self.dataAccess._scanCWD)
        self.dataAccess.fileCreated.connect(self.onImageFileCreate)
        self.dataAccess.loadList.connect(self.dataAccess._loadList)
        self.dataAccess.scanList.connect(self.dataAccess._scanList)
        self.dataThread.start()
        self.dataAccess.moveToThread(self.dataThread)

        self.dataAdapter = DataAdapter.DataAdapter()
        self.model = DataModel.DataModel(self)
        self.proxyModel = ProxyModel.ProxyModel(self)
        self.proxyModel.setSourceModel(self.model)

        # Instatiate and set toolbar for containing buttons
        self.toolBar = QtWidgets.QToolBar(self)
        # self.toolBar.setStyleSheet("QToolButton{margin: 0px 10px;}")
        self.toolBar.setFixedWidth(self.width())
        self.toolBar.setFloatable(False)
        self.toolBar.setMovable(False)
        self.toolBar.setMaximumWidth(self.maximumWidth())
        self.toolBar.setFixedWidth(35)
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        # Instantiate tabWidget and add it to the mainLayout
        self.tabWidget = TabWidget.TabWidget(self.mainWidget)
        self.tabWidget.welcomePage.newFolderClicked.connect(self.selectDirectory)
        self.tabWidget.welcomePage.newFileClicked.connect(self.selectFile)
        self.tabWidget.welcomePage.loadListClicked.connect(self.loadList)
        self.tabWidget.welcomePage.lastSessionClicked.connect(self.loadLastSession)
        self.tabWidget.welcomePage.recentPathsClicked.connect(self.loadPath)
        self.mainLayout.addWidget(self.tabWidget)
        self.mainLayout.addWidget(self.tabWidget.mainStatusBar)

        # Instantiate a dockwidget object for holding the listView, and connect its signals
        self.dockWidget = DockWidget.DockWidget("Image List", self, QtCore.Qt.Widget)
        self.dockWidget.setStyleSheet(style)
        self.dockWidget.directoryTable.setModel(self.proxyModel)
        self.dockWidget.directoryTable.clicked.connect(self.tabWidget.openImage)
        self.dockWidget.directoryTable.listOrderChanged.connect(self.model.reOrganizeData)
        self.dockWidget.directoryTable.mouseMiddleButtonClicked.connect(self.tabWidget.openNewImageTab)
        self.dockWidget.searchBox.textChanged.connect(self.proxyModel.searchModel)
        self.dockWidget.searchBox.returnPressed.connect(self.returnKeyFunc)

        # Instantiate push buttons and add buttons to the toolbar
        self.addTabButton = QtWidgets.QToolButton(self.tabWidget)
        self.addTabButton.setIcon(QtGui.QIcon("icons/add2.svg"))
        self.addTabButton.setIconSize(QtCore.QSize(24, 24))
        self.addTabButton.setShortcut("Ctrl+T")

        self.toggleListAction = self.toolBar.addAction(QtGui.QIcon("icons/image_list.svg"), "Open/Close Image List")
        self.toggleListAction.setShortcut("L")
        self.toggleListAction.triggered.connect(self.toggleList)

        self.searchListAction = self.toolBar.addAction(QtGui.QIcon("icons/image_search.svg"), "Search Image List")
        self.searchListAction.setShortcut("Ctrl+F")
        self.searchListAction.triggered.connect(self.searchList)

        self.toolBar.addSeparator()

        self.openDirAction = self.toolBar.addAction(QtGui.QIcon("icons/folder.svg"), "Open Folder")
        self.openDirAction.setShortcut("Ctrl+O")
        self.openDirAction.triggered.connect(self.selectDirectory)

        self.addFileAction = self.toolBar.addAction(QtGui.QIcon("icons/add_image.svg"), "Add Image")
        self.addFileAction.setShortcut("Ctrl+I")
        self.addFileAction.triggered.connect(self.selectFile)

        self.deleteFileAction = self.toolBar.addAction(QtGui.QIcon("icons/remove.svg"), "Remove Image")
        self.deleteFileAction.setShortcut("Ctrl+D")
        self.deleteFileAction.triggered.connect(self.removeFile)

        self.toolBar.addSeparator()

        self.saveListAction = self.toolBar.addAction(QtGui.QIcon("icons/save.svg"), "Save Image List")
        self.saveListAction.setShortcut("Ctrl+S")
        self.saveListAction.triggered.connect(self.saveList)

        self.loadListAction = self.toolBar.addAction(QtGui.QIcon("icons/load.svg"), "Load Image List")
        self.loadListAction.setShortcut("Ctrl+L")
        self.loadListAction.triggered.connect(self.loadList)

        self.spacer = QtWidgets.QWidget()
        self.spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.toolBar.addWidget(self.spacer)

        self.moreAction = self.toolBar.addAction(QtGui.QIcon("icons/more_icon.svg"), "More")
        self.moreAction.triggered.connect(self.onMoreButtonClick)

        # Add a corner widget to tabView and instantiated buttons to toolbar
        self.tabWidget.setCornerWidget(self.addTabButton, QtCore.Qt.TopRightCorner)
        self.addTabButton.clicked.connect(self.tabWidget.addNewTab)

        self.toolBar.setContentsMargins(0, 0, 0, 0)
        self.toolBar.setIconSize(QtCore.QSize(30, 30))

        # self.mainLayout.addWidget(self.dockWidget)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockWidget)
        # self.dockWidget.setFloating(True)

        self.openAction = QtWidgets.QAction("Open Image")
        self.openAction.setIcon(QtGui.QIcon("icons/open.svg"))
        self.openAction.triggered.connect(self.openSelected)

        self.openInNewTabAction = QtWidgets.QAction("Open Image in New tab")
        self.openInNewTabAction.setIcon(QtGui.QIcon("icons/open_in_new_tab.svg"))
        self.openInNewTabAction.triggered.connect(self.openSelectedInTab)

        self.addTagAction = QtWidgets.QAction("Add New Tag")
        self.addTagAction.setIcon(QtGui.QIcon("icons/tag.svg"))
        self.addTagAction.triggered.connect(self.addTag)

        self.deleteTagAction = QtWidgets.QAction("Clear Tags")
        self.deleteTagAction.setIcon(QtGui.QIcon("icons/remove_tag.svg"))
        self.deleteTagAction.triggered.connect(self.deleteTag)

        self.dockWidget.directoryTable.addAction(self.openAction)
        self.dockWidget.directoryTable.addAction(self.openInNewTabAction)
        self.dockWidget.directoryTable.addAction(self.deleteFileAction)
        self.dockWidget.directoryTable.addAction(self.addTagAction)
        self.dockWidget.directoryTable.addAction(self.deleteTagAction)

        self.dockWidgetShown = False
        self.recentDirectories = list()
        self.readSettings()

    # Handle keyPressEvent
    def keyPressEvent(self, event):
        # Exit app
        if event.key() == QtCore.Qt.Key_Escape:
            if self.dockWidget.searchBox.isVisible():
                self.dockWidget.searchBox.hide()
                self.proxyModel.searchModel('')

            elif self.isFullScreen():
                self.dockWidget.show()
                self.toolBar.show()
                self.tabWidget.tabBar().show()
                self.showNormal()

            else:
                self.close()

        if event.key() == QtCore.Qt.Key_W:
            # Ctrl+W closes current tab
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.tabWidget.tabCloseRequested.emit(self.tabWidget.currentIndex())
            else:
                self.tabWidget.currentWidget().keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Space:
            self.tabWidget.currentWidget().keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Left:
            self.leftKeyFunc()

        if event.key() == QtCore.Qt.Key_Right:
            self.rightKeyFunc()

        if event.key() == QtCore.Qt.Key_Q:
            self.tabWidget.currentWidget().keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_S:
            self.tabWidget.currentWidget().keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_R:
            if event.modifiers() & QtCore.Qt.ControlModifier:
                self.loadLastSession()

        if event.key() == QtCore.Qt.Key_F:
            if not self.isFullScreen():
                self.dockWidgetShown = self.dockWidget.isVisible()
                self.dockWidget.hide()
                self.toolBar.hide()
                self.tabWidget.tabBar().hide()
                self.tabWidget.mainStatusBar.hide()
                self.showFullScreen()

            else:
                self.toolBar.show()
                self.tabWidget.mainStatusBar.show()
                self.tabWidget.tabBar().show()
                if self.dockWidgetShown:
                    self.dockWidget.show()
                self.showNormal()

        if event.key() == QtCore.Qt.Key_Tab:
            event.ignore()

    # Handle ResizeEvent
    def resizeEvent(self, event):
        self.toolBar.resize(35, event.size().height())
        self.toolBar.updateGeometry()

    # Opens directory
    def selectDirectory(self):
        fileDialog = QtWidgets.QFileDialog(self)
        selectedDirectory = fileDialog.getExistingDirectory(self, "Open Directory", None,
                                                            fileDialog.DontResolveSymlinks)
        if self.dataAccess.setDirectory(selectedDirectory) is not False:
            self.model.clearModel()
            self.recentDirectories.append(selectedDirectory)
            if self.dockWidget.isHidden():
                self.dockWidget.show()
            self.dataAccess.scan.emit()

    # Adds selected file to listView
    def selectFile(self):
        fileDialog = QtWidgets.QFileDialog(self)
        selectedFileDir = fileDialog.getOpenFileNames(self, fileDialog.tr("Open Image File"),
                                                      fileDialog.tr("/test/FolderTest"), fileDialog.tr(
                "Images (*.png *.jpg *.jpeg *.bmp *.gif *.pbm *.pgm *.ppm *.xbm *.xpm)"))
        if selectedFileDir[0] != '':
            if self.dockWidget.isHidden():
                self.dockWidget.show()
            print(self.thread().objectName())
            self.dataAccess.scanList.emit(selectedFileDir[0])

    # Saves list info in json format
    def saveList(self):
        fileDialog = QtWidgets.QFileDialog(self)
        fileName = fileDialog.getSaveFileName(self, fileDialog.tr("Save Image List"), fileDialog.tr("List Name"))
        self.dataAccess.saveList.emit(fileName[0], self.model.displayedList())

    # Loads json formatted list save file
    def loadList(self):
        fileDialog = QtWidgets.QFileDialog(self)
        selectedFileDir = fileDialog.getOpenFileName(self, fileDialog.tr("Open List"),
                                                     fileDialog.tr("/test/FolderTest"),
                                                     fileDialog.tr("Image List (*.ive)"))
        if selectedFileDir[0] != '':
            self.model.clearModel()
            if self.dockWidget.isHidden():
                self.dockWidget.show()
            imageJsonList = self.dataAccess.loadList.emit(selectedFileDir[0])

    def loadPath(self, path):
        if self.dataAccess.setDirectory(path) is not False:
            self.model.clearModel()
            if self.dockWidget.isHidden():
                self.dockWidget.show()
            self.recentDirectories.append(path)
            self.dataAccess.scan.emit()

    def loadLastSession(self):
        print("load last session")

    def toggleList(self):
        if self.dockWidget.isVisible():
            self.dockWidget.hide()

        else:
            self.dockWidget.show()

    # Removes selected file from listView and model
    def removeFile(self):
        selectedIndex = self.dockWidget.getDirectoryList().currentIndex()
        if selectedIndex.isValid():
            fileRow = selectedIndex.row()
            self.model.removeImage(fileRow)
            self.updateStatusBar()

    def searchList(self):
        if self.dockWidget.searchBox.isHidden():
            self.dockWidget.searchBox.show()
            self.dockWidget.searchBox.setFocus(QtCore.Qt.ActiveWindowFocusReason)

        else:
            self.dockWidget.searchBox.setFocus(QtCore.Qt.ActiveWindowFocusReason)

        self.updateStatusBar()

    def openSelected(self):
        self.tabWidget.openImage(self.dockWidget.directoryTable.currentIndex())

    def openSelectedInTab(self):
        self.tabWidget.openNewImageTab(self.dockWidget.directoryTable.currentIndex())

    def addTag(self):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setLabelText("Enter new tag:")
        dialog.setInputMode(QtWidgets.QInputDialog.TextInput)
        dialog.setWindowFlag(QtCore.Qt.FramelessWindowHint, True)
        palette = Palette.Palette()
        palette.setBrush(QtGui.QPalette.Text, QtGui.QBrush(QtGui.QColor(255, 255, 255, 100)))
        # dialog.setPalette(palette)
        dialog.open()
        dialog.textValueSelected.connect(self.changeTag)

    def changeTag(self, text):
        index = self.dockWidget.directoryTable.currentIndex()
        self.model.addTag(text, index)

    def deleteTag(self):
        index = self.dockWidget.directoryTable.currentIndex()
        self.model.clearTag(index)

    # Function that is run when left key is pressed
    def leftKeyFunc(self):
        if self.model.rowCount(0) != 0:
            previousIndex = None
            # Get current selected index
            currentIndex = self.dockWidget.directoryTable.currentIndex()
            currentRow = currentIndex.row()

            # If it is topmost index get bottom index as previous index
            if currentRow == 0:
                previousIndex = currentIndex.siblingAtRow(self.proxyModel.rowCount(currentIndex) - 1)

            else:
                previousIndex = currentIndex.siblingAtRow(currentRow - 1)

            # Get index displayed and set selected index as previousIndex
            self.tabWidget.openImage(previousIndex)
            self.dockWidget.directoryTable.setCurrentIndex(previousIndex)

    # Function that is run when right key is pressed
    def rightKeyFunc(self):
        if self.model.rowCount(0) != 0:
            nextIndex = None
            # Get current selected index
            currentIndex = self.dockWidget.directoryTable.currentIndex()
            currentRow = currentIndex.row()

            # If it is bottommost index, get the topmost index as next index
            totalRow = self.proxyModel.rowCount(currentIndex)
            if currentRow == self.proxyModel.rowCount(currentIndex) - 1:
                nextIndex = currentIndex.siblingAtRow(0)

            else:
                nextIndex = currentIndex.siblingAtRow(currentRow + 1)

            # Get index displayed and set selected index as nextIndex
            self.tabWidget.openImage(nextIndex)
            self.dockWidget.directoryTable.setCurrentIndex(nextIndex)

    def returnKeyFunc(self):
        if self.dockWidget.directoryTable.currentIndex().isValid():
            self.rightKeyFunc()
        else:
            firstIndex = self.proxyModel.index(0, 0)
            if firstIndex.isValid():
                self.tabWidget.openImage(firstIndex)
                self.dockWidget.directoryTable.selectRow(firstIndex.row())

    def mouseDoubleClickEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            openPage = self.tabWidget.currentWidget()
            doubleClickedObject = None
            doubleClickedPos = self.childAt(event.pos())
            if doubleClickedPos is not None:
                doubleClickedObject = doubleClickedPos.parent()
            if openPage is doubleClickedObject:
                if not self.isFullScreen():
                    self.dockWidgetShown = self.dockWidget.isVisible()
                    self.dockWidget.hide()
                    self.toolBar.hide()
                    self.tabWidget.mainStatusBar.hide()
                    self.tabWidget.tabBar().hide()
                    self.showFullScreen()

                else:
                    self.toolBar.show()
                    self.tabWidget.mainStatusBar.show()
                    self.tabWidget.tabBar().show()
                    if self.dockWidgetShown:
                        self.dockWidget.show()
                    self.showNormal()

        super().mouseDoubleClickEvent(event)

    # index is the parent index
    def updateStatusBar(self, index=None, first=None, last=None):
        self.dockWidget.showMessage(
            self.dataAccess.directory() + " " + str(self.model.rowCount(self.proxyModel.index(0, 0))) + " Images")

    def onImageFileCreate(self, imageList, loadingStatus):
        objectList = self.dataAdapter.convert(imageList)
        self.model.addImage(objectList)
        if self.tabWidget.currentWidget() is self.tabWidget.welcomePage:
            self.tabWidget.openNewImageTab(self.model.index(0, 0), True)

        currentStatus = self.dockWidget.progressBar.value()
        if currentStatus == -1:
            self.dockWidget.progressBar.show()

        if currentStatus != loadingStatus and loadingStatus % 10 == 0:
            self.updateStatusBar()
            self.dockWidget.progressBar.setValue(loadingStatus)
            if loadingStatus == 100:
                self.dockWidget.progressBar.reset()
                self.dockWidget.progressBar.hide()

    def onMoreButtonClick(self):
        asd = QtWidgets.QMenu()
        a1 = QtWidgets.QAction("Show Buffer View")
        a2 = QtWidgets.QAction("Show Buffer View")
        asd.addAction(a1)
        asd.addAction(a2)
        widget = self.toolBar.widgetForAction(self.moreAction)
        print(widget.pos(), widget.mapToGlobal(widget.pos()))
        asd.exec_(widget.mapToGlobal(widget.pos()))
        print("fill this button")

    # parameters QCloseEvent event
    def closeEvent(self, event):
        self.writeSettings()
        self.dataThread.quit()
        self.dataThread.wait()
        super().closeEvent(event)

    def readSettings(self):
        settings = QtCore.QSettings("Cave VFX", "Ive")
        if settings.contains("dataAccess/path"):
            path = settings.value("dataAccess/path")
            self.dataAccess.setDirectory(path)

        if settings.contains("dockWidget/floating"):
            floating = False
            if settings.value("dockWidget/floating") == "true":
                floating = True
            self.dockWidget.setFloating(floating)

        if settings.contains("dockWidget/position"):
            position = settings.value("dockWidget/position")
            self.dockWidget.move(position)

        if settings.contains("dockWidget/size"):
            size = settings.value("dockWidget/size")
            self.dockWidget.resize(size)

        if settings.contains("mainWindow/fullScreen"):
            fullScreen = False
            if settings.value("mainWindow/fullScreen") == "true":
                fullScreen = True

            if fullScreen:
                self.showFullScreen()

        if settings.contains("mainWindow/maximized"):
            maximized = False
            if settings.value("mainWindow/maximized") == "true":
                maximized = True
            if maximized:
                self.showMaximized()

        if settings.contains("mainWindow/position"):
            position = settings.value("mainWindow/position")
            self.move(position)

        if settings.contains("mainWindow/size"):
            size = settings.value("mainWindow/size")
            self.resize(size)

        if settings.contains("recentDirs"):
            recentDirs = settings.value("recentDirs")
            if recentDirs is not None:
                if type(recentDirs) is str:
                    self.recentDirectories.append(recentDirs)

                else:
                    for i in range(len(recentDirs)):
                        if i < 4:
                            self.recentDirectories.append(recentDirs.pop())
                        else:
                            break
                self.tabWidget.welcomePage.setRecentDirectories(self.recentDirectories)

    def writeSettings(self):
        settings = QtCore.QSettings("Cave VFX", "Ive")
        settings.setValue("mainWindow/maximized", self.isMaximized())
        settings.setValue("dockWidget/position", self.dockWidget.pos())
        settings.setValue("dockWidget/floating", self.dockWidget.isFloating())
        settings.setValue("dockWidget/size", self.dockWidget.size())
        settings.setValue("dataAccess/path", self.dataAccess.directory())
        settings.setValue("mainWindow/fullScreen", self.isFullScreen())
        recentList = list()
        for i in range(len(self.recentDirectories)):
            if i < 4:
                recentList.append(self.recentDirectories.pop())
            else:
                break
        settings.setValue("recentDirs", recentList)

        if self.isFullScreen() or self.isMaximized():
            self.showNormal()
            settings.setValue("mainWindow/size", self.size())
            settings.setValue("mainWindow/position", self.pos())
        else:
            settings.setValue("mainWindow/position", self.pos())
            settings.setValue("mainWindow/size", self.size())
