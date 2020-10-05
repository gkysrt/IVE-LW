import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import TableView
import TableViewDelegate
import Palette

class DockWidget(QtWidgets.QDockWidget):

    def __init__(self, title = None, parent = None, flags = None):
        super(DockWidget, self).__init__(title, parent, flags)
        #self.setPalette(Palette.Palette())
        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea | QtCore.Qt.BottomDockWidgetArea)  #Dockwidget can be on rightside or leftside of the mainwindow
        self.setMinimumWidth(20)                #Set minimum size

        self.setFocusPolicy(QtCore.Qt.NoFocus)        
        self.wrapperWidget = QtWidgets.QWidget(self)
        self.wrapperLayout = QtWidgets.QVBoxLayout(self.wrapperWidget)
        self.wrapperLayout.setContentsMargins(0, 0, 0, 0)
        self.wrapperLayout.setSpacing(0)
        self.wrapperWidget.setContentsMargins(0, 0, 0, 0)

        self.dockStatusBar = QtWidgets.QWidget(self.wrapperWidget)
        self.dockStatusBarLayout = QtWidgets.QHBoxLayout(self.dockStatusBar)
        self.dockStatusBarLayout.setContentsMargins(0, 0, 0, 0)
        self.dockStatusBar.setContentsMargins(0, 0, 0, 0)
        self.dockStatusBar.setFixedHeight(20)

        self.progressBar = QtWidgets.QProgressBar(self.dockStatusBar)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setFixedWidth(80)
        self.progressBar.setRange(0, 100)
        self.progressBar.setTextVisible(False)
        self.progressBar.hide()

        self.textLabel = QtWidgets.QLabel(self.dockStatusBar)
        self.textLabel.setMargin(0)
        self.textLabel.setContentsMargins(6, 0, 0, 0)
        self.textLabel.setMaximumWidth(self.dockStatusBar.maximumWidth())

        self.textLabel.setMinimumWidth(20)
        self.dockStatusBarLayout.addWidget(self.progressBar)
        self.dockStatusBarLayout.addWidget(self.textLabel)

        #Instantiate tableView
        self.directoryTable = TableView.TableView(self.wrapperWidget)
        self.directoryTableDelegate = TableViewDelegate.TableViewDelegate(self.directoryTable)
        self.directoryTable.setItemDelegate(self.directoryTableDelegate)
        self.directoryTable.resizeRowsToContents()
        self.directoryTable.resizeColumnsToContents()
        #self.directoryTable.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

        self.directoryTable.verticalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        self.directoryTable.verticalHeader().hide()
        self.wrapperLayout.addWidget(self.directoryTable)
        self.wrapperLayout.addWidget(self.dockStatusBar)

        #Instantiate and set searchBox
        self.searchBox = QtWidgets.QLineEdit(self)
        self.searchBox.setClearButtonEnabled(True)
        self.searchBox.setPlaceholderText("Search Image...")
        self.searchBox.addAction(QtGui.QIcon("icons/search.svg"), QtWidgets.QLineEdit.LeadingPosition)
        self.searchBox.resize(self.size().width(), 18)
        self.searchBox.setFrame(False)
        self.searchBox.setStyleSheet("QLineEdit {background-color: lightgray;  selection-background-color: #585A5B; font-family:'Arial'; font-size:9pt; color: '#3E3F40'}")
        self.searchBox.hide()

        self.setWidget(self.wrapperWidget)
        self.hide()

    def getDirectoryList(self):
        return self.directoryTable

    def resizeEvent(self, event):
        self.searchBox.resize(event.size().width(), 18)
        self.dockStatusBar.resize(event.size().width(), 20)
        super(DockWidget, self).resizeEvent(event)


    def showMessage(self, message):
        self.textLabel.setText(message)
        self.textLabel.repaint()
