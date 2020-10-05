import PySide2.QtCore as QtCore
import PySide2.QtWidgets as QtWidgets
import PySide2.QtGui as QtGui
import math

class SplitterItem(QtWidgets.QGraphicsObject):

    splitterItemChanged = QtCore.Signal(object, float)

    def __init__(self, rect, parent = None):
        super(SplitterItem, self).__init__(parent)

        #Customize initial situation
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemClipsToShape, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIgnoresParentOpacity, True)
        self.setBoundingRegionGranularity(1)
        #Create shape and bounding rect of SplitterItem
        self.itemShape = QtGui.QPainterPath()
        self.itemBoundingRect = rect

        self.centralRect = QtCore.QRect(self.itemBoundingRect.x(), self.itemBoundingRect.y(), 20, 20)
        self.centralRect.moveCenter(self.itemBoundingRect.center())
        self.moveTextRect = QtCore.QRect(self.centralRect.center().x(), self.centralRect.center().y() - 20, 80, 20)

        self.upperVerticalStick = QtCore.QRect(self.itemBoundingRect.x() + self.itemBoundingRect.center().x() - 1, self.itemBoundingRect.y() + 10, 3, (self.itemBoundingRect.height() - self.centralRect.height()) / 2 - 10)
        self.lowerVerticalStick = QtCore.QRect(self.itemBoundingRect.x() + self.itemBoundingRect.center().x() - 1, self.itemBoundingRect.y() + self.upperVerticalStick.height() + self.centralRect.height() + 10, 3, (self.itemBoundingRect.height() - self.centralRect.height()) / 2)
        self.rotationStick = QtCore.QRect(self.itemBoundingRect.x() + self.itemBoundingRect.center().x() + 11, self.itemBoundingRect.y() + self.itemBoundingRect.center().y() - 2, self.itemBoundingRect.center().y() - 10, 5)
        self.rotationTextRect = QtCore.QRect(self.itemBoundingRect.x() + self.itemBoundingRect.center().x() + self.rotationStick.width() - 10, self.itemBoundingRect.y() + self.itemBoundingRect.center().y() - 20, 27, 15)
        self.opacityRect = QtCore.QRect(self.itemBoundingRect.x() + 10, self.itemBoundingRect.y() + 10, 30, 30)
        self.opacityTextRect = QtCore.QRect(self.itemBoundingRect.x() + 15 + self.opacityRect.width(), self.itemBoundingRect.y(), 35, 15)
        self.changeSceneRect = QtCore.QRect(self.itemBoundingRect.x() + self.itemBoundingRect.width() - 30, self.itemBoundingRect.y() + 10, 20, 20)

        self.setTransformOriginPoint(self.centralRect.center())

        #Instantiate a rect and pen for QPainter
        self.brush = QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern)

        #Customize itemShape
        self.itemShape.addRect(self.rotationStick)
        self.itemShape.addRect(self.upperVerticalStick)
        self.itemShape.addRect(self.lowerVerticalStick)
        self.itemShape.addRect(self.centralRect)
        self.itemShape.addRect(self.opacityRect)
        self.itemShape.addRect(self.changeSceneRect)

        self.centerPoint = self.mapToScene(self.transformOriginPoint())

        self.originalX = self.scenePos().x()
        self.originalY = self.scenePos().y()

        self.rotationMode = False
        self.opacityMode = False
        self.moveMode = False
        self.changeSceneMode = False

        self.opacityClickPos = 0

        self.textBackgroundColor = QtGui.QColor(25, 27, 29, 11)

    def paint(self, painter, option, widget):
        painter.save()
        painter.fillRect(self.rotationStick, QtCore.Qt.darkRed)
        painter.fillRect(self.upperVerticalStick, QtCore.Qt.darkRed)
        painter.fillRect(self.lowerVerticalStick, QtCore.Qt.darkRed)
        opacity = int(self.parentItem().opacity()*100)
        opacityColor = QtGui.QColor(150 - 0.22 * opacity,87 - 0.87 * opacity,0,255)
        painter.fillRect(self.opacityRect, opacityColor)
        painter.fillRect(self.changeSceneRect, QtCore.Qt.darkRed)
        painter.fillRect(self.centralRect, QtCore.Qt.darkRed)
        fontMetric = painter.fontMetrics()

        if(self.opacityMode):
            font = painter.font()
            font.setPointSize(10)
            font.setFamily("Arial")
            painter.setPen(opacityColor)
            painter.setFont(font)
            painter.drawText(self.opacityTextRect, str(opacity)[:4]+"%")

        if(self.rotationMode):
            font = painter.font()
            font.setPointSize(10)
            font.setFamily("Arial")
            painter.setPen(QtCore.Qt.darkRed)
            painter.setFont(font)
            rotation = str(int(self.rotation()))
            painter.drawText(self.rotationTextRect, QtCore.Qt.AlignRight, rotation[:4]+ "\xb0")

        if(self.moveMode):
            font = painter.font()
            font.setPointSize(10)
            font.setFamily("Arial")
            painter.setPen(QtCore.Qt.darkRed)
            painter.setFont(font)
            rotation = str(int(self.rotation()))
            position = self.mapToScene(self.transformOriginPoint())
            x = str(int(position.x()))
            y = str(int(position.y()))
            positionText = x + ", " + y
            painter.drawText(self.moveTextRect, QtCore.Qt.AlignRight, fontMetric.elidedText(positionText, QtCore.Qt.ElideRight, self.moveTextRect.width()))
        painter.restore()

    def itemChange(self, change, value):
        if ((change is self.ItemPositionHasChanged) or (change is self.ItemRotationHasChanged)):
            #Gives position change
            if(change is self.ItemPositionHasChanged):
                self.centerPoint = self.mapToScene(self.transformOriginPoint())
            self.splitterItemChanged.emit(change, value)
        return value

    def getSplitterCenter(self):
        return self.centerPoint

    def setSplitterCenter(self, point):
        self.setPos(point.x() - self.boundingRect().width() / 2, point.y() - self.boundingRect().height() / 2)

    def shape(self):
        return self.itemShape

    #Override boundingRect func
    def boundingRect(self):
        return self.itemBoundingRect

    #Override setBoundingRect func
    def setBoundingRect(self, rect):
        self.prepareGeometryChange()
        self.itemBoundingRect = rect

    #Shows and enables splitter item
    def showSplitter(self):
        self.show()
        self.setEnabled(True)

    #Hides and disables splitter item
    def hideSplitter(self):
        self.hide()
        self.setEnabled(False)

    def mousePressEvent(self, event):
        if (self.rotationStick.adjusted(0, -4, 8, 6).contains(event.pos().toPoint())):
            self.setFlag(self.ItemClipsToShape, False)

            if ((event.buttons() & QtCore.Qt.LeftButton) and (event.modifiers() & QtCore.Qt.ShiftModifier)):
                self.rotationMode = True

            elif (event.button() is QtCore.Qt.LeftButton):
                self.rotationMode = True

        elif (self.opacityRect.contains(event.pos().toPoint())):
            if(event.button() is QtCore.Qt.LeftButton):
                self.setFlag(self.ItemClipsToShape, False)
                self.opacityClickPos = event.pos()
                self.opacityMode = True
                self.splitterItemChanged.emit(70, 0)

        elif(self.changeSceneRect.contains(event.pos().toPoint())):
            if(event.button() is QtCore.Qt.LeftButton):
                self.splitterItemChanged.emit(90, 0)
                self.changeSceneMode = True
        else:
            if(self.centralRect.contains(event.pos().toPoint()) or self.lowerVerticalStick.contains(event.pos().toPoint()) or self.upperVerticalStick.contains(event.pos().toPoint())):
                self.moveMode = True
                self.setFlag(self.ItemClipsToShape, False)

            super(SplitterItem, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if (self.opacityMode is True):
            if (event.buttons() & QtCore.Qt.LeftButton):
                pos = self.mapToParent(event.pos())

                yOffset = self.mapToParent(self.opacityClickPos).y() - pos.y()
                self.splitterItemChanged.emit(50, yOffset)

        elif (self.rotationMode is True):
            if (event.buttons() & QtCore.Qt.LeftButton):
                pos = self.mapToScene(event.pos())
                origin = self.mapToScene(self.transformOriginPoint())
                rotationPoint = QtCore.QPointF(pos.x() - origin.x(), pos.y() - origin.y())
                rotationPointRadius = math.sqrt(math.pow(rotationPoint.x(), 2) + math.pow(rotationPoint.y(), 2))
                cosDegree = math.degrees(math.acos(rotationPoint.x()/rotationPointRadius))
                sinDegree = math.degrees(math.asin(rotationPoint.y()/rotationPointRadius))
                #If mouse is above origin point
                if(event.modifiers() & QtCore.Qt.ShiftModifier):
                    if(int(round(cosDegree%45)) < 5):
                        coefficient = int(cosDegree/45)
                        if(sinDegree < 0):
                            self.setRotation(360 - coefficient * 45)
                        else:
                            self.setRotation(coefficient * 45)

                    elif(int(round(cosDegree%45)) > 40):
                        coefficient = int(cosDegree/45) + 1
                        if(sinDegree < 0):
                            self.setRotation(360 - coefficient * 45)
                        else:
                            self.setRotation(coefficient * 45)
                else:
                    if(sinDegree < 0):
                        self.setRotation(360 - cosDegree)
                    else:
                        self.setRotation(cosDegree)
        elif(self.changeSceneMode is True):
            pass
        else:
            super(SplitterItem, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if(event.button() is QtCore.Qt.LeftButton):
            if(self.rotationMode is True):
                self.setFlag(self.ItemClipsToShape, True)
                self.rotationMode = False

            if(self.opacityMode is True):
                self.opacityMode = False
                self.splitterItemChanged.emit(70, 0)
                self.setFlag(self.ItemClipsToShape, True)

            if(self.moveMode is True):
                self.moveMode = False
                self.setFlag(self.ItemClipsToShape, True)
            
            if(self.changeSceneMode is True):
                self.changeSceneMode = False
        super(SplitterItem, self).mouseReleaseEvent(event)

    def hoverEnterEvent(self, event):
        if(self.rotationStick.adjusted(0, -4, 8, 6).contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)

        elif(self.upperVerticalStick.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.lowerVerticalStick.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.centralRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.changeSceneRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.PointingHandCursor)

        elif(self.opacityRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeVerCursor)

        super(SplitterItem, self).hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        if(self.rotationStick.adjusted(0, -4, 8, 6).contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.CursorShape.SizeVerCursor)

        elif(self.upperVerticalStick.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.lowerVerticalStick.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.centralRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeAllCursor)

        elif(self.changeSceneRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.PointingHandCursor)

        elif(self.opacityRect.contains(event.pos().toPoint())):
            self.setCursor(QtCore.Qt.SizeVerCursor)
        super(SplitterItem, self).hoverMoveEvent(event)