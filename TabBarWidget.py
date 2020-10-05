from PySide2 import QtGui, QtCore, QtWidgets


class ButtonTabBar(QtWidgets.QTabBar):
    newTabClicked = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAutoHide(True)
        self.__addTabButton = QtWidgets.QPushButton(self)
        self.__addTabButton.setParent(self.parent())
        self.__addTabButton.setFixedSize(QtCore.QSize(self.height(), self.height()))
        self.__addTabButton.clicked.connect(self.newTabClicked.emit)
        self.__addTabButton.setIconSize(QtCore.QSize(18, 18))
        self.__addTabButton.setStyleSheet("QPushButton{"
                                          "background-color:rgb(50, 50, 50);"
                                          "border: 1px solid rgb(50, 50, 50);"
                                          "border-radius: 4px;"
                                          "font-size:14px;"
                                          "qproperty-icon: url(icons/add.svg);}"
                                          "QPushButton:hover:!pressed{"
                                          "background-color: rgb(80, 75, 75);}"
                                          "QPushButton:pressed{"
                                          "background-color:rgb(90, 85, 85);"
                                          "color:rgb(250, 175, 0);}")
        self.moveAddTabButton()

    def sizeHint(self):
        sizeHint = QtWidgets.QTabBar.sizeHint(self)
        width = sizeHint.width()
        height = sizeHint.height()
        return QtCore.QSize(width, height)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.moveAddTabButton()

    def tabLayoutChange(self):
        super().tabLayoutChange()
        self.moveAddTabButton()

    def moveAddTabButton(self):
        # width of all tabs
        size = sum([self.tabRect(i).width() for i in range(self.count())])
        h = (self.geometry().bottom() - self.__addTabButton.height())
        w = self.width()
        if size > w:
            self.__addTabButton.move(w - self.__addTabButton.width(), h)
        else:
            self.__addTabButton.move(size, h)

    def button(self):
        return self.__addTabButton
