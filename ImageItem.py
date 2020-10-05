import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import os
import math
import time


class ImageItem(QtWidgets.QGraphicsItem):
    def __init__(self, rect, bufferName, filePath=None, parent=None):
        super(ImageItem, self).__init__(parent)
        # Get bufferName
        self.bufferName = bufferName

        # Set some parameters for items to execute initially
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)

        # Set a classwise brush and pen for items
        self.brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 125), QtCore.Qt.SolidPattern)
        self.pen = QtGui.QPen(self.brush, 1, QtCore.Qt.PenStyle.SolidLine, QtCore.Qt.PenCapStyle.FlatCap,
                              QtCore.Qt.RoundJoin)

        # Assignments with given func parameters
        self.filePath = filePath  # filePath of pixmap
        self.rect = rect  # Item's bufferView rect
        lazyImage = QtGui.QImageReader(self.filePath)
        lazyImage.setAutoTransform(True)

        self.__originalImage = lazyImage.read()  # Pixmap in the middle of the items

        # Some classwise variables to use
        self.wCoefficient = None  # Width coefficient of pixmap
        self.hCoefficient = None  # Height coefficient of pixmap
        self.bufferView = True
        self.textRectangle = QtCore.QRect(self.rect.x(), self.rect.height() + self.rect.y() + 5, self.rect.width(),
                                          30)  # Text's rect
        self.closeRectangle = QtCore.QRect(self.rect.x() + self.rect.width() - 30, self.rect.y() - 30, 30, 30)
        self.itemBoundingRect = self.rect

        self.itemShape = QtGui.QPainterPath()
        self.defaultShape = True

        self.__bufferPixmapRectangle = None  # Pixmap's rect

        self.image = None
        self.imageMode = None  # == 0 R-channel, == 1 G-channel, == 2 B-channel, 3 Grayscaled

        # If a filePath is given initially
        if filePath is not None:
            if self.image is not None:
                if self.imageMode == 0:
                    self.showRChannel()
                elif self.imageMode == 1:
                    self.showGChannel()
                elif self.imageMode == 2:
                    self.showBChannel()
                elif self.imageMode == 3:
                    self.showGrayScaled()
            # Get image's size
            width = self.__originalImage.size().width()
            height = self.__originalImage.size().height()

            # Calculate width and height coefficients
            self.wCoefficient = self.rect.width() / width
            self.hCoefficient = self.rect.width() / height

            # If height/width ratio of the frame rect is lower than pixmap's ratio
            # __bufferPixmapRectangle's width will be calculated and height stays the same
            if self.rect.height() / self.rect.width() < height / width:
                # Calculate a rect that'll fit in ImageItem's bounding rect and center it
                self.__bufferPixmapRectangle = QtCore.QRect(0, 0,
                                                            self.rect.width() * self.hCoefficient / self.wCoefficient,
                                                            self.rect.height())
                self.__bufferPixmapRectangle.moveCenter(self.rect.center())

            # If pixmap's h/w ratio is lower
            # __bufferPixmapRectangle's height will be calculated and width stays the same
            else:
                # Calculate a rect that'll fit in ImageItem's bounding rect and center it
                self.__bufferPixmapRectangle = QtCore.QRect(0, 0, self.rect.width(),
                                                            self.rect.height() * self.wCoefficient / self.hCoefficient)
                self.__bufferPixmapRectangle.moveCenter(self.rect.center())

    # Function to get filePath from outside to set shown image,
    # If image is changed while bufferView item's bounding rect doesn't need to change
    # Otherwise, with every pixmap a new bounding rect should be assigned
    # Sending 'None' instead of filePath, clears this buffer
    def setImage(self, filePath):
        # Load pixmap and get image's size
        self.filePath = filePath
        if filePath is None:
            self.__bufferPixmapRectangle = None
            return
        lazyImage = QtGui.QImageReader(filePath)
        lazyImage.setAutoTransform(True)
        self.__originalImage = lazyImage.read()
        if self.image is not None:
            if self.imageMode == 0:
                self.showRChannel()
            elif self.imageMode == 1:
                self.showGChannel()
            elif self.imageMode == 2:
                self.showBChannel()
            elif self.imageMode == 3:
                self.showGrayScaled()
        width = self.__originalImage.size().width()
        height = self.__originalImage.size().height()

        # Calculate width and height coefficients
        self.wCoefficient = self.rect.width() / width
        self.hCoefficient = self.rect.height() / height

        # If height/width ratio of the frame rect is lower than pixmap's ratio
        # __bufferPixmapRectangle's width will be calculated and height stays the same
        if self.rect.height() / self.rect.width() < height / width:
            # Calculate a rect that'll fit in ImageItem's bounding rect and center it
            self.__bufferPixmapRectangle = QtCore.QRect(0, 0, self.rect.width() * self.hCoefficient / self.wCoefficient,
                                                        self.rect.height())
            self.__bufferPixmapRectangle.moveCenter(self.rect.center())

        # If pixmap's h/w ratio is lower
        # __bufferPixmapRectangle's height will be calculated and width stays the same
        else:
            # Calculate a rect that'll fit in ImageItem's bounding rect and center it
            self.__bufferPixmapRectangle = QtCore.QRect(0, 0, self.rect.width(),
                                                        self.rect.height() * self.wCoefficient / self.hCoefficient)
            self.__bufferPixmapRectangle.moveCenter(self.rect.center())

        if self.bufferView is False:
            self.prepareGeometryChange()
            self.itemBoundingRect = self.__originalImage.rect()

    # Override GraphicsItem's paint function
    def paint(self, painter, option, widget):
        painter.save()
        # painter.setBackgroundMode(QtCore.Qt.OpaqueMode)
        painter.setPen(self.pen)
        fontMetric = painter.fontMetrics()
        # If rect drawing is needed draw rect and text
        if self.bufferView:
            # If it is bufferView it means that two buffers are on display
            painter.fillRect(self.rect, QtGui.QColor(255, 255, 255, 20))

            if self.filePath is not None:
                font = painter.font()
                font.setPointSize(11)
                font.setFamily("Arial")
                painter.setFont(font)

                # Text is currently outside item's bounding rect (by 35 y value)
                painter.drawText(self.textRectangle, QtGui.QTextOption.WordWrap | QtCore.Qt.AlignLeft,
                                 fontMetric.elidedText(os.path.basename(self.filePath), QtCore.Qt.ElideRight,
                                                       self.textRectangle.width() * 5 / 7))
                painter.drawText(self.textRectangle, QtGui.QTextOption.WordWrap | QtCore.Qt.AlignRight,
                                 fontMetric.elidedText(str(self.__originalImage.rect().width()) + "x" + str(
                                     self.__originalImage.rect().height()), QtCore.Qt.ElideRight,
                                                       self.textRectangle.width() * 2 / 7))
                if self.image is not None:
                    painter.drawImage(self.__bufferPixmapRectangle, self.image)
                else:
                    painter.drawImage(self.__bufferPixmapRectangle, self.__originalImage)
            else:

                font = painter.font()
                font.setPointSize(80)
                font.setFamily("Arial")
                painter.setFont(font)
                painter.drawText(self.rect, QtCore.Qt.AlignCenter, self.bufferName)

        else:
            # If no bufferView it means the picture is on display
            if self.filePath is not None:
                # font = painter.font()
                # font.setPixelSize(75)
                # font.setFamily("Arial")
                # painter.setFont(font)
                if self.image is not None:
                    painter.drawImage(self.__originalImage.rect(), self.image)
                else:
                    painter.drawImage(self.__originalImage.rect(), self.__originalImage)

                # painter.drawText(self.__pixmap.rect().adjusted(0, -125, 0, 0), QtGui.QTextOption.WordWrap | QtCore.Qt.AlignLeft, fontMetric.elidedText(os.path.basename(self.filePath), QtCore.Qt.ElideRight, self.__pixmap.rect().width()))
                # painter.drawText(self.__pixmap.rect().adjusted(0, self.__pixmap.rect().height() + 200, 0, 0), QtGui.QTextOption.WordWrap | QtCore.Qt.AlignLeft, fontMetric.elidedText(str(self.__pixmap.rect().width()) + "x" + str(self.__pixmap.rect().height()), QtCore.Qt.ElideRight, self.__pixmap.rect().width()))
        painter.restore()

    def shape(self):
        if self.defaultShape:
            return super(ImageItem, self).shape()

        else:
            return self.itemShape

    # Enable - disable function for bufferView painting ops
    def setBufferViewEnabled(self, enabled):
        self.prepareGeometryChange()

        if enabled:
            self.bufferView = True
            self.itemBoundingRect = self.rect
            self.setCursor(QtCore.Qt.PointingHandCursor)
        else:
            self.bufferView = False
            if self.filePath is not None:
                self.itemBoundingRect = self.pixmapRect()
                self.setCursor(QtCore.Qt.OpenHandCursor)

    def bufferRect(self):
        return self.rect

    def setBufferRect(self, rect):
        self.rect = rect

    # Set item's bounding rect
    def setBoundingRect(self, rect):
        self.prepareGeometryChange()
        self.itemBoundingRect = rect

    # Return item's bounding rect
    def boundingRect(self):
        return self.itemBoundingRect

    # Return pixmap's bounding rect
    def pixmapRect(self):
        return self.__originalImage.rect()

    def bufferPixmapRect(self):
        return self.__bufferPixmapRectangle

    def pixmap(self):
        return self.__originalImage

    # On drop event
    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            self.filePath = event.mimeData().urls().pop().path()

        else:
            self.filePath = os.path.abspath(event.mimeData().text())  # Get dropped file's text (filePath)
        self.setImage(self.filePath)  # Set shown image
        # self.scene().update(self.itemBoundingRect)
        self.scene().update(self.rect)  # Update item's bounding rect
        self.scene().update(self.textRectangle)  # Update text's bounding rect
        super(ImageItem, self).dropEvent(event)

    def showRChannel(self):
        image = QtGui.QImage(self.__originalImage)
        self.imageMode = 0
        memoryData = image.bits()
        redList = memoryData[2::4]
        self.image = QtGui.QImage(redList.tobytes(), self.__originalImage.width(), self.__originalImage.height(),
                                  self.__originalImage.width(), QtGui.QImage.Format_Grayscale8)

    def showGChannel(self):
        image = QtGui.QImage(self.__originalImage)
        self.imageMode = 1
        memoryData = image.bits()
        greenList = memoryData[1::4]
        self.image = QtGui.QImage(greenList.tobytes(), self.__originalImage.width(), self.__originalImage.height(),
                                  self.__originalImage.width(), QtGui.QImage.Format_Grayscale8)

    def showBChannel(self):
        image = QtGui.QImage(self.__originalImage)
        self.imageMode = 2
        memoryData = image.bits()
        blueList = memoryData[::4]
        self.image = QtGui.QImage(blueList.tobytes(), self.__originalImage.width(), self.__originalImage.height(),
                                  self.__originalImage.width(), QtGui.QImage.Format_Grayscale8)

    def showGrayScaled(self):
        image = QtGui.QImage(self.__originalImage)
        self.imageMode = 3
        self.image = image.convertToFormat(QtGui.QImage.Format_Grayscale8)

    def showColorful(self):
        self.image = None
        self.imageMode = None

    def changeDefaultShape(self, shape, enabled):
        self.itemShape = shape
        self.defaultShape = not enabled

    # Overload of changeDefaultShape func
    def setDefaultShapeEnabled(self, enabled):
        self.defaultShape = enabled

    def dragEnterEvent(self, event):
        self.setOpacity(0.8)
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        self.setOpacity(1)
        super().dragLeaveEvent(event)

    def hoverEnterEvent(self, event):
        if self.bufferView:
            self.setOpacity(0.8)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if self.bufferView:
            self.setOpacity(1)
        super().hoverLeaveEvent(event)
