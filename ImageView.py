import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui

import ImageItem
import SplitterItem
import math
import RGBAWidget

class ImageView(QtWidgets.QGraphicsView):

    #Signal to be emitted whenever a pixmap in buffer changes
    #Parameters: fileName = File Name of new pixmap
    bufferPixmapChanged = QtCore.Signal(str)
    imageZoomChanged = QtCore.Signal(int)

    def __init__(self, parent = None):
        super(ImageView, self).__init__(parent)
        #Background variables
        self.setCursor(QtCore.Qt.ArrowCursor)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)

        self.backgroundColor = QtGui.QColor(30, 30, 30, 255)
       # self.backgroundColor.setHsv(215, 37, 29)
        self.backgroundBrush = QtGui.QBrush()
        self.backgroundBrush.setColor(self.backgroundColor)
        self.backgroundBrush.setStyle(QtCore.Qt.SolidPattern)
        self.setBackgroundBrush(self.backgroundBrush)

        #Set the scene for this QGraphicsView
        self.scene = QtWidgets.QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHints(QtGui.QPainter.HighQualityAntialiasing | QtGui.QPainter.SmoothPixmapTransform | QtGui.QPainter.TextAntialiasing)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)

        self.customContextMenuRequested.connect(self.showMenu)

        #This QGraphicsView is aligned on center of its parent
        # and initially it is in NoDrag mode
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setTransformationAnchor(self.AnchorUnderMouse)

        #Both itemA and B (bufferA and B) are items within given rectangles
        self.itemA = ImageItem.ImageItem(QtCore.QRect(45, 30, 320, 180), "A")
        self.itemB = ImageItem.ImageItem(QtCore.QRect(410, 30, 320, 180), "B")
        self.itemA.setZValue(1)

        #Instantiate SplitterItem and make it disabled initially
        self.splitterItem = SplitterItem.SplitterItem(QtCore.QRect(0, 0, 160, 160), self.itemA)
        self.splitterItem.hideSplitter()    #Hidden initially
        self.splitterItem.setZValue(2)  #SplitterItem is on top
        self.splitterOnCenter = True

        #Add these items to the scene
        self.scene.addItem(self.itemA)
        self.scene.addItem(self.itemB)

        #Set scene rect this given rect so that items can be seen better
        self.setSceneRect(QtCore.QRect(0,0,775,240))

        #Initially selected buffer is A and program is in bufferView
        self.selectedA = True
        self.bufferView = True
        self.splitterView = False

        #View is not scaled initially so scaleHint is 1
        self.scaleHint = 1

        #FitInViewMode
        self.fitInViewModeA = True
        self.fitInViewModeB = True

        self.splitterItem.splitterItemChanged.connect(self.onSplitterItemChange)
        self.splitterFullScene = True

        self.rot = 0
        self.itemOpacity = 1

        #For dragging splitterItem with the press of mouse middle button
        self.middleClickPos = None
        self.splitterPos = None

        self.lastScaleA = None
        self.lastCenterA = None

        self.lastScaleB = None
        self.lastCenterB = None

        self.rgbaWidget = RGBAWidget.RGBAWidget(self)
        self.rgbaWidgetShown = False
        self.leftViewport = False
        self.imageData = None
        self.secondImageData = None

        self.bufferViewContextMenu = QtWidgets.QMenu("Image", self)
        self.menuDisplayAction = QtWidgets.QAction("Display Image")
        self.menuClearAction = QtWidgets.QAction("Clear Buffer")

        self.bufferViewContextMenu.addAction(self.menuDisplayAction)
        self.bufferViewContextMenu.addAction(self.menuClearAction)

        self.imageViewContextMenu = QtWidgets.QMenu("Image", self)
        self.menuBufferViewAction = QtWidgets.QAction("Show Buffer View")
        self.menuSplitterViewAction = QtWidgets.QAction("Show/Hide Splitter")
        self.menuFitInViewAction = QtWidgets.QAction("Fit in View")
        self.menuRealSizeAction = QtWidgets.QAction("Show Real Size")
        self.menuZoomInAction = QtWidgets.QAction("Zoom in")
        self.menuZoomOutAction = QtWidgets.QAction("Zoom out")

        self.imageViewContextMenu.addAction(self.menuBufferViewAction)
        self.imageViewContextMenu.addAction(self.menuSplitterViewAction)
        self.imageViewContextMenu.addSeparator()
        self.imageViewContextMenu.addAction(self.menuRealSizeAction)
        self.imageViewContextMenu.addAction(self.menuFitInViewAction)
        self.imageViewContextMenu.addAction(self.menuZoomInAction)
        self.imageViewContextMenu.addAction(self.menuZoomOutAction)
        self.imageViewContextMenu.addSeparator()

        self.scheduledZoomValues = list()
        self.scheduledZoom = 0

    def loadImage(self, fileName):
        #If bufferA is the current buffer..
        if (self.selectedA):
            self.itemA.setImage(fileName)
            if (self.splitterView):
                self.showSplitterView()
            else:
                self.showBufferA()
                self.bufferPixmapChanged.emit(fileName)

        #If current buffer is not bufferA,
        else:
            self.itemB.setImage(fileName)
            self.showBufferB()

        #Update scene part where the items are
        self.scene.update(self.scene.itemsBoundingRect())

    #Injection func. for fitInView
    def fitImage(self, rect = None):
        #If no argument is given, fits in self.sceneRect()
        if (rect == None):
            self.fitInView(self.sceneRect(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        #If an argument is given, fits in argument rect
        else:
            self.fitInView(rect, QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        self.scaleHint = self.matrix().m11()    #Get horizontal scaling factor
        self.splitterItem.setScale(1 / self.scaleHint)
        self.imageZoomChanged.emit(self.scaleHint*100)

    def showRealSize(self):
        self.zoom(1 / self.scaleHint)
        if(self.selectedA):
            self.fitInViewModeA = False

        else:
            self.fitInViewModeB = False

    #Function to show bufferA
    def showBufferA(self):
        bufferView = bool(self.bufferView)

        if(self.itemA.bufferPixmapRect() is None):
            return

        self.splitterView = False
        self.splitterItem.hideSplitter()
        self.selectedA = True   #bufferA is selected
        self.bufferView = False #bufferView is no more
        self.itemB.setVisible(False)    #bufferB shouldn't be visible
        self.itemB.setEnabled(False)    #bufferB shouldn't be enabled
        self.itemA.setBufferViewEnabled(False)    #bufferA's surrounding rect etc. shouldn't be enabled
        self.setBackgroundBrush(QtCore.Qt.black)
        #If currently no pixmap loaded into rect

        #Show item's bounding rect
        self.setSceneRect(self.itemA.boundingRect())
        if (self.fitInViewModeA):
            self.fitImage(self.itemA.boundingRect())

        elif(self.lastScaleA is not None):
            if(bufferView is True):
                currScale = self.matrix().m11()    #Get horizontal scaling factor
                self.scale(1/currScale, 1/currScale) #Reset current scale and make it 1
                self.scale(self.lastScaleA, self.lastScaleA)
                self.scaleHint = float(self.lastScaleA)
                self.splitterItem.setScale(1/self.scaleHint)
                self.centerOn(self.lastCenterA)
                self.imageZoomChanged.emit(self.scaleHint*100)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.itemA.setFlag(self.itemA.ItemClipsToShape, False)
        self.itemA.setDefaultShapeEnabled(True)
        self.itemA.setOpacity(1)

    #Function to show bufferB
    def showBufferB(self):
        bufferView = bool(self.bufferView)
        if(self.itemB.bufferPixmapRect() is None):
            return

        self.splitterView = False
        self.splitterItem.hideSplitter()
        self.selectedA = False  #bufferA is no more
        self.bufferView = False #bufferView is no more
        self.itemA.setVisible(False) #bufferA shouldn't be visible
        self.itemA.setEnabled(False) #bufferA shouldn't be enabled
        self.itemB.setBufferViewEnabled(False) #bufferB's surrounding rect etc. shouldn't be enabled
        self.setBackgroundBrush(QtCore.Qt.black)

        #Show item's bounding rect
        self.setSceneRect(self.itemB.boundingRect())
        if (self.fitInViewModeB):
            self.fitImage(self.itemB.boundingRect())

        elif(self.lastScaleB is not None):
            if(bufferView is True):
                currScale = self.matrix().m11()    #Get horizontal scaling factor
                self.scale(1/currScale, 1/currScale)
                self.scale(self.lastScaleB, self.lastScaleB)
                self.scaleHint = float(self.lastScaleB)
                self.splitterItem.setScale(1/self.scaleHint)
                self.centerOn(self.lastCenterB)
                self.imageZoomChanged.emit(self.scaleHint*100)

        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.itemA.setFlag(self.itemA.ItemClipsToShape, False)
        self.itemA.setDefaultShapeEnabled(True)
        self.itemA.setOpacity(1)
        self.itemB.setOpacity(1)

    #Function to show bufferView
    def showBufferView(self):
        #If bufferA was last selected and not was in bufferView
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        if(self.selectedA and not self.bufferView):
            self.lastScaleA = float(self.scaleHint)
            self.lastCenterA = QtCore.QPointF(self.mapToScene(self.viewport().rect().center()))

        #If bufferB was last selected and not was in bufferView
        if(not self.selectedA and not self.bufferView):
            self.lastScaleB = float(self.scaleHint)
            self.lastCenterB = QtCore.QPointF(self.mapToScene(self.viewport().rect().center()))

        self.splitterView = False
        self.splitterItem.hideSplitter()
        self.itemA.setBufferViewEnabled(True) #bufferA's surrounding rect etc. enabled, changed boundingRect
        self.itemB.setBufferViewEnabled(True) #bufferB's surrounding rect etc. enabled, changed boundingRect
        self.itemA.setVisible(True) #bufferA is visible
        self.itemA.setEnabled(True) #bufferA is enabled
        self.itemB.setVisible(True) #bufferB is visible
        self.itemB.setEnabled(True) #bufferB is enabled
        self.setSceneRect(QtCore.QRect(0,0,775,240)) #Scene rect is set to full view rect
        self.fitImage(QtCore.QRect(0,0,775,240))    #Fit view according to full view rect
        self.bufferView = True                      #current view is bufferView
        self.itemA.setFlag(self.itemA.ItemClipsToShape, False)
        self.itemA.setDefaultShapeEnabled(True)
        self.setBackgroundBrush(self.backgroundBrush)
        self.itemA.setOpacity(1)

        #Calling setDragMode(self.ScrollHandDrag) once more fixes a cursor shape problem for no reason?
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        self.setCursor(QtCore.Qt.ArrowCursor)

    def showSplitterView(self):
        bufferView = bool(self.bufferView)
        if(self.itemA.bufferPixmapRect() is None):
            return
        if(self.lastScaleA is not None):
            self.splitterItem.setScale(1 / self.scaleHint)

        self.splitterView = True
        self.bufferView = False
        self.selectedA = True

        self.itemA.setVisible(True)
        self.itemA.setEnabled(True)
        self.itemA.setBufferViewEnabled(False)
        self.itemA.setFlag(self.itemA.ItemClipsToShape, True)

        self.itemB.setVisible(True)
        self.itemB.setEnabled(True)
        self.itemB.setBufferViewEnabled(False)
        self.setBackgroundBrush(QtCore.Qt.black)

        self.splitterItem.showSplitter()
        if(self.fitInViewModeA):
            self.fitImage()
        self.onSplitterItemChange(self.splitterItem.ItemPositionHasChanged, self.mapToScene(self.splitterItem.pos().toPoint()))
        if(self.splitterFullScene):
            self.setSceneRect(self.itemA.boundingRect().united(self.itemB.boundingRect()))
            self.scene.update(self.itemA.boundingRect().united(self.itemB.boundingRect()))

        else:
            self.setSceneRect(self.itemA.boundingRect())
            self.scene.update(self.itemA.boundingRect())

        self.itemA.setOpacity(self.itemOpacity)
        self.itemB.setOpacity(1)
        self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        #If splitter is opened for the first time or splitterOnCenter is set to true, set splitter on the center of the view
        if(self.splitterOnCenter):
            self.splitterItem.setSplitterCenter(self.mapToScene(self.viewport().rect().center()))
            self.splitterOnCenter = False

    def keyPressEvent(self, event):
        #Left, Right, W, Escape keys ignored for the parent class to deal with.
        if (event.key() == QtCore.Qt.Key_R):
            if(not self.bufferView):
                if(self.selectedA):
                    self.itemA.showRChannel()
                else:
                    self.itemB.showRChannel()
                self.scene.update()

        if (event.key() == QtCore.Qt.Key_G):
            if(not self.bufferView):
                if(self.selectedA):
                    self.itemA.showGChannel()
                else:
                    self.itemB.showGChannel()
                self.scene.update()

        if (event.key() == QtCore.Qt.Key_B):
            if(not self.bufferView):
                if(self.selectedA):
                    self.itemA.showBChannel()
                else:
                    self.itemB.showBChannel()
            self.scene.update()

        if(event.key() == QtCore.Qt.Key_H):
            if(not self.bufferView):
                if(self.selectedA):
                    self.itemA.showGrayScaled()
                else:
                    self.itemB.showGrayScaled()

                self.scene.update()

        if(event.key() == QtCore.Qt.Key_C):
            if(not self.bufferView):
                if(self.selectedA):
                    self.itemA.showColorful()
                else:
                    self.itemB.showColorful()
                self.scene.update()

        if (event.key() == QtCore.Qt.Key_Left):
            event.ignore()

        if (event.key() == QtCore.Qt.Key_Right):
            event.ignore()

        if (event.key() == QtCore.Qt.Key_W):
            if(event.modifiers() & QtCore.Qt.ControlModifier):
                event.ignore()
                return
            #If view is buffer view fit in view key does not work
            if(not self.bufferView):

                #If looking at bufferA and already fit in view, quit fitInView mode
                if(self.selectedA and self.fitInViewModeA):
                    self.fitInViewModeA = False

                #If looking at bufferA and not fit in view, fit the view and enter fitInView mode
                elif (self.selectedA and not self.fitInViewModeA):
                    self.fitInViewModeA = True
                    self.fitImage()

                #If not looking at bufferA (it's bufferB) and it's in fitInViewMode, quit fitInViewMode
                elif (not self.selectedA and self.fitInViewModeB):
                    self.fitInViewModeB = False

                #If not looking at bufferA (bufferB) and it's not in fitInView mode, fit it - enter fitInView mode
                elif (not self.selectedA and not self.fitInViewModeB):
                    self.fitInViewModeB = True
                    self.fitImage()

        if (event.key() == QtCore.Qt.Key_F):
            event.ignore()

        if (event.key() == QtCore.Qt.Key_Escape):
            event.ignore()

        if (event.key() == QtCore.Qt.Key_S):
            if(self.splitterView is False):
                if(event.modifiers() & QtCore.Qt.ShiftModifier):
                    self.splitterOnCenter = True
                self.showSplitterView()

            else:
                self.showBufferA()

        if (event.key() == QtCore.Qt.Key_Q):
            if(not self.bufferView):
                self.showRealSize()

        #Space key is accepted, and if it is bufferView show bufferA,
        # if it is bufferA or bufferB view, show bufferView
        if (event.key() == QtCore.Qt.Key_Space):
            event.accept()
            if(self.bufferView == False):
                self.showBufferView()
            else:
                self.showBufferA()

        if (event.key() == QtCore.Qt.Key_Tab):
            event.ignore()

    #TODO: Make mouse zoom able to return pic percentage
    def wheelEvent(self, event):
        if (self.bufferView is False):
            rotation = event.delta() #Most mouses have 15 cycle stages and this function returns 120
            # numDegrees = event.delta() / 8
            # numSteps = numDegrees / 15
            # self.scheduledZoom += numSteps
            # self.scheduledZoomValues.append(numSteps)
            # print(self.scheduledZoom)
            # anim = QtCore.QTimeLine(360, self)
            # anim.setUpdateInterval(20)
            #
            # anim.valueChanged.connect(self.zoomWithAnimation)
            # anim.finished.connect(self.zoomAnimationFinished)
            # anim.start()

            if(self.selectedA):
                self.fitInViewModeA = False

            else:
                self.fitInViewModeB = False

            itemOnDisplay = self.itemB
            if(self.selectedA):
                itemOnDisplay = self.itemA

            #If rotation is forward..
            if (rotation > 0):
                #..and scale hint is below x20..
                if(self.scaleHint < 20):
                    #..recalculate scale hint and scale the picture by 120/110(most cases)
                    self.zoom(rotation/114)

            #If the wheel rotation is backwards..
            elif (rotation < 0):
                #..and scale hint is above 0.4..
                if(((self.scaleHint * 114/-rotation) * itemOnDisplay.pixmapRect().width() >  16) and ((self.scaleHint * 114/-rotation) * itemOnDisplay.pixmapRect().height() >  16)):
                    #..recalculate scale hint and scale the picture by 110/120(most cases)
                    self.zoom(114/-rotation)

    # def zoomWithAnimation(self):
    #     factor = 1 + self.scheduledZoom / 360
    #     self.zoom(factor)
    #
    # def zoomAnimationFinished(self):
    #     pass
       # self.scheduledZoom -= self.scheduledZoomValues.pop(0)

        # if self.scheduledZoom > 0:
        #     self.scheduledZoom -= 1
        # else:
        #     self.scheduledZoom += 1


    def zoom(self, coefficient = None):
        if(not self.bufferView):
            if(coefficient == None):
                if(self.selectedA):
                    if(self.fitInViewModeA):
                        self.showRealSize()
                    else:
                        self.fitInViewModeA = True
                        self.fitImage()
                else:
                    if(self.fitInViewModeB):
                        self.showRealSize()
                    else:
                        self.fitInViewModeB = True
                        self.fitImage()

            else:
                self.scale(coefficient, coefficient)
                self.scaleHint = self.scaleHint * coefficient
                self.splitterItem.setScale(1/self.scaleHint)
                self.imageZoomChanged.emit(self.scaleHint*100)

    def mousePressEvent(self, event):
        #Moving the splitter by dragging mouse middle button on the image
        if (event.button() == QtCore.Qt.MiddleButton):
            if (self.splitterView is True):
                self.middleClickPos = event.pos()
                self.splitterPos = self.splitterItem.pos()

        #Handling pixel examining window
        if(not self.bufferView):
            if((event.buttons() & QtCore.Qt.RightButton) and (event.modifiers() & QtCore.Qt.SHIFT)):
                #calling scrollhanddrag one more time magically fixes cursor problem once more
                self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
                self.setCursor(QtCore.Qt.CrossCursor)
                if(not self.splitterView):
                    self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                    self.rgbaWidget.show()
                    self.rgbaWidgetShown = True

                    if(self.selectedA):
                        self.imageData = self.itemA.pixmap().toImage()

                    else:
                        self.imageData = self.itemB.pixmap().toImage()

                    pos = self.mapToScene(event.pos()).toPoint()
                    buffer = "B"
                    if(self.selectedA):
                        buffer = "A"
                    if(self.imageData.rect().contains(pos)):
                        rgb = self.imageData.pixelColor(pos)
                        if(self.selectedA):
                            self.rgbaWidget.setValues(buffer, rgb.red(), rgb.green(), rgb.blue(), str(pos.x()) + "," + str(pos.y()))

                        else:
                            self.rgbaWidget.setValues(buffer, rgb.red(), rgb.green(), rgb.blue(), str(pos.x()) + "," + str(pos.y()))

                    else:
                        self.rgbaWidget.setValues(buffer, "N/A", "N/A", "N/A", "N/A")
                else:
                    if(self.itemA.bufferPixmapRect() is None or self.itemB.bufferPixmapRect() is None):
                        self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                    else:
                        self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 340, 110)

                    self.rgbaWidget.show()
                    self.rgbaWidgetShown = True
                    self.imageData = self.itemA.pixmap().toImage()
                    self.secondImageData = self.itemB.pixmap().toImage()
                    pos = self.mapToScene(event.pos()).toPoint()

                    if((self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill) and self.imageData.rect().contains(pos)) and self.secondImageData.rect().contains(pos)):
                        rgbA = self.imageData.pixelColor(pos)
                        rgbB = self.secondImageData.pixelColor(pos)
                        self.rgbaWidget.setValues("A", rgbA.red(), rgbA.green(), rgbA.blue(), str(pos.x()) + "," + str(pos.y()), "B", rgbB.red(), rgbB.green(), rgbB.blue(), str(pos.x()) + "," + str(pos.y()))

                    elif(self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill) and self.imageData.rect().contains(pos)):
                        rgbA = self.imageData.pixelColor(pos)
                        self.rgbaWidget.setValues("A", rgbA.red(), rgbA.green(), rgbA.blue(), str(pos.x()) + "," + str(pos.y()))
                        self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                    elif(self.secondImageData.rect().contains(pos)):
                        rgbB = self.secondImageData.pixelColor(pos)
                        self.rgbaWidget.setValues("B", rgbB.red(), rgbB.green(), rgbB.blue(), str(pos.x()) + "," + str(pos.y()))
                        self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                    else:
                        self.rgbaWidget.setValues("A", "N/A", "N/A", "N/A", "N/A", "B", "N/A", "N/A", "N/A", "N/A")
        super(ImageView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if(event.buttons() & QtCore.Qt.MiddleButton):
            if(self.splitterView is True):
                movedPos = event.pos()
                self.splitterItem.setPos(self.splitterPos.x() + (movedPos.x() - self.middleClickPos.x()) / self.scaleHint, self.splitterPos.y() + (movedPos.y() - self.middleClickPos.y()) / self.scaleHint)

        if(self.rgbaWidgetShown):
            if(not (event.modifiers() & QtCore.Qt.ShiftModifier)):
                self.rgbaWidget.close()
                self.rgbaWidgetShown = False
                self.leftViewport = False
                self.setCursor(QtCore.Qt.ArrowCursor)
                self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                return

            if(not self.viewport().rect().contains(event.pos())):
                self.rgbaWidget.close()
                self.leftViewport = True

            elif(self.viewport().rect().contains(event.pos()) and self.leftViewport):
                self.rgbaWidget.show()
                self.leftViewport = False

            if(not self.splitterView):
                self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)
                pos = self.mapToScene(event.pos()).toPoint()
                buffer = "A"
                if(not self.selectedA):
                    buffer = "B"

                if(self.imageData.rect().contains(pos)):
                    rgb = self.imageData.pixelColor(pos)
                    self.rgbaWidget.setValues(buffer, rgb.red(), rgb.green(), rgb.blue(), str(pos.x()) + "," + str(pos.y()))

                else:
                    self.rgbaWidget.setValues(buffer, "N/A", "N/A", "N/A", "N/A")

            else:
                pos = self.mapToScene(event.pos()).toPoint()

                #If itemA or B is None, RGBA Widget size should be arranged for one buffer only
                if(self.itemB.bufferPixmapRect() is None or self.itemB.bufferPixmapRect() is None):
                    self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                #If mouse pos is not on itemA and on itemB, RGBA Widget size should be arranged for one buffer only
                elif ((not self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill)) and (self.secondImageData.rect().contains(pos))):
                    self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                #If mouse pos is not on itemB and on itemA, RGBA Widget size should be arranged for one buffer only
                elif ((self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill) and (self.imageData.rect().contains(pos))) and (not self.secondImageData.rect().contains(pos))):
                    self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 170, 110)

                #On other conditions (out of scene, both on A and B etc.), RGBA widget size should be arranged for two buffers
                else:
                    self.rgbaWidget.setGeometry(event.globalX(), event.globalY(), 340, 110)

                #If cursor is on both of the buffers
                if((self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill) and self.imageData.rect().contains(pos)) and self.secondImageData.rect().contains(pos)):
                    rgbA = self.imageData.pixelColor(pos)
                    rgbB = self.secondImageData.pixelColor(pos)
                    self.rgbaWidget.setValues("A", rgbA.red(), rgbA.green(), rgbA.blue(), str(pos.x()) + "," + str(pos.y()), "B", rgbB.red(), rgbB.green(), rgbB.blue(), str(pos.x()) + "," + str(pos.y()))

                #If cursor is on A only
                elif(self.shapePolygon.containsPoint(pos, QtCore.Qt.OddEvenFill) and (self.imageData.rect().contains(pos))):
                    rgbA = self.imageData.pixelColor(pos)
                    self.rgbaWidget.setValues("A", rgbA.red(), rgbA.green(), rgbA.blue(), str(pos.x()) + "," + str(pos.y()))

                #If cursor is on B only
                elif(self.secondImageData.rect().contains(pos)):
                    rgbB = self.secondImageData.pixelColor(pos)
                    self.rgbaWidget.setValues("B", rgbB.red(), rgbB.green(), rgbB.blue(), str(pos.x()) + "," + str(pos.y()))

                else:
                    self.rgbaWidget.setValues("A", "N/A", "N/A", "N/A", "N/A", "B", "N/A", "N/A", "N/A", "N/A")


        super(ImageView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if(self.rgbaWidgetShown):
            self.rgbaWidget.close()
            self.rgbaWidgetShown = False
            self.leftViewport = False
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

        #Handling of the clicks on buffers when the view is bufferView
        #If mouse press is left button
        if (event.button() == QtCore.Qt.LeftButton):
            #And if the view is bufferView
            if (self.bufferView is True):

                #If it's on bufferA (Left rectangle), show bufferA
                if(self.itemA.contains(self.mapToScene(event.pos()))):
                    self.showBufferA()

                #If it's on bufferB (Right rectangle), show bufferB
                elif(self.itemB.contains(self.mapToScene(event.pos()))):
                    self.showBufferB()

        super().mouseReleaseEvent(event)

    def dragEnterEvent(self, event):
        #View state records if the scene is in bufferView or not before any change
        self.viewState = bool(self.bufferView)
        self.splitterState = bool(self.splitterView)
        if not self.bufferView:
            self.showBufferView()

        super(ImageView, self).dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        #On drag leave, if bufferA was fullscreen and bufferView was not shown
        #return to bufferA view
        if (self.selectedA is True and self.viewState is False):
            if(self.splitterState):
                self.showSplitterView()
            else:
                self.showBufferA()

        #Else, show bufferView
        else:
            self.showBufferView()

        return super().dragLeaveEvent(event)

    def dropEvent(self, event):
        #If mouse dropped on bufferA, emit signal that
        #its pixmap has changed and send data of new picture's fileName
        super(ImageView, self).dropEvent(event)#Running children dropEvents first.
        if(self.itemA.contains(self.mapToScene(event.pos()))):
            newTabTitle = event.mimeData().text()
            if(event.mimeData().hasUrls()):
                newTabTitle = event.mimeData().urls().pop().path()
            self.bufferPixmapChanged.emit(newTabTitle)

        if(self.selectedA and self.viewState is False):
            if(self.splitterState):
                self.showSplitterView()
            else:
                self.showBufferA()

    def onSplitterItemChange(self, change, value):
        if (change == 90):
            if(self.splitterFullScene):
                self.setSceneRect(self.itemA.boundingRect())
                self.splitterFullScene = False
            else:
                self.setSceneRect(self.itemA.boundingRect().united(self.itemB.boundingRect()))
                self.splitterFullScene = True
        if (change == 70):
            self.itemOpacity = self.itemA.opacity()

        if(change == 50):
            currentOpacity = self.itemA.opacity()
            self.itemA.setOpacity(self.itemOpacity + value/250 * self.scaleHint)

        if ((change is QtWidgets.QGraphicsItem.ItemRotationHasChanged) or (change is QtWidgets.QGraphicsItem.ItemPositionHasChanged)):
            shape = QtGui.QPainterPath()
            self.shapePolygon = QtGui.QPolygonF()
            self.shapePolygon.resize(4)

            if(change is QtWidgets.QGraphicsItem.ItemRotationHasChanged):
                self.rot = value

            if(self.rot % 360 == 0):
                self.shapePolygon[0] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.scenePos().y())
                self.shapePolygon[1] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x(), self.itemA.scenePos().y())
                self.shapePolygon[2] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x(), self.itemA.boundingRect().height())
                self.shapePolygon[3] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.boundingRect().height())

            elif(self.rot % 360 == 90):
                self.shapePolygon[0] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.scenePos().y())
                self.shapePolygon[1] = QtCore.QPointF(self.itemA.boundingRect().width(), self.itemA.scenePos().y())
                self.shapePolygon[2] = QtCore.QPointF(self.itemA.boundingRect().width(), self.splitterItem.getSplitterCenter().y())
                self.shapePolygon[3] = QtCore.QPointF(self.itemA.scenePos().x(), self.splitterItem.getSplitterCenter().y())

            elif(self.rot % 360 == 270):
                self.shapePolygon[0] = QtCore.QPointF(self.itemA.scenePos().x(), self.splitterItem.getSplitterCenter().y())
                self.shapePolygon[1] = QtCore.QPointF(self.itemA.boundingRect().width(), self.splitterItem.getSplitterCenter().y())
                self.shapePolygon[2] = QtCore.QPointF(self.itemA.boundingRect().width(), self.itemA.boundingRect().height() + 1)
                self.shapePolygon[3] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.boundingRect().height() + 1)


            elif((0 < self.rot % 360 < 90) or (270 < self.rot % 360 < 360)):
                self.shapePolygon[0] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.scenePos().y())
                self.shapePolygon[1] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x() + (self.splitterItem.getSplitterCenter().y() * math.tan(math.radians(self.rot))), self.itemA.scenePos().y())
                self.shapePolygon[2] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x() - ((self.itemA.boundingRect().height() - self.splitterItem.getSplitterCenter().y()) * math.tan(math.radians(self.rot))), self.itemA.boundingRect().height())
                self.shapePolygon[3] = QtCore.QPointF(self.itemA.scenePos().x(), self.itemA.boundingRect().height())
            else:
                self.shapePolygon[0] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x() + (self.splitterItem.getSplitterCenter().y() * math.tan(math.radians(self.rot))), self.itemA.scenePos().y())
                self.shapePolygon[1] = QtCore.QPointF(self.itemA.boundingRect().width() + 3, self.itemA.scenePos().y())
                self.shapePolygon[2] = QtCore.QPointF(self.itemA.boundingRect().width() + 3, self.itemA.boundingRect().height())
                self.shapePolygon[3] = QtCore.QPointF(self.splitterItem.getSplitterCenter().x() - ((self.itemA.boundingRect().height() - self.splitterItem.getSplitterCenter().y()) * math.tan(math.radians(self.rot))), self.itemA.boundingRect().height())

            shape.closeSubpath()
            shape.addPolygon(self.shapePolygon)
            self.itemA.changeDefaultShape(shape, True)
        self.scene.update(self.itemA.boundingRect().united(self.itemB.boundingRect()))

    def resizeEvent(self, event):
        #If the view is fitInViewA and looking at bufferA or
        #If the view is fitInViewB and looking at bufferB or
        #If the view is in bufferView
        if ((self.fitInViewModeA and self.selectedA) or (self.fitInViewModeB and not self.selectedA) or self.bufferView):
            self.fitImage() #Fit the scene

        else:
            #TODO: Need to find a better method to update the view
            self.scale(0.99, 0.99)
            self.scale(100/99, 100/99)

    def showMenu(self, pos):
        if(self.rgbaWidgetShown is not True):
            if(self.bufferView):
                #Rather than binding actions to functions, actions are handled here
                if(self.itemA.contains(self.mapToScene(pos)) and self.itemA.bufferPixmapRect() is not None):
                    action = self.bufferViewContextMenu.exec_(self.mapToGlobal(pos))

                    if(action is self.menuClearAction):
                        self.itemA.setImage(None)
                        self.bufferPixmapChanged.emit("Empty Tab")

                    if(action is self.menuDisplayAction):
                        self.showBufferA()

                if(self.itemB.contains(self.mapToScene(pos)) and self.itemB.bufferPixmapRect() is not None):
                    action = self.bufferViewContextMenu.exec_(self.mapToGlobal(pos))

                    if(action is self.menuClearAction):
                        self.itemB.setImage(None)

                    if(action is self.menuDisplayAction):
                        self.showBufferB()

            elif(not self.bufferView):
                action = self.imageViewContextMenu.exec_(self.mapToGlobal(pos))
                if(action is self.menuBufferViewAction):
                    self.showBufferView()
                if(action is self.menuSplitterViewAction):
                    self.showSplitterView()
                if(action is self.menuFitInViewAction):
                    self.fitImage()
                if(action is self.menuRealSizeAction):
                    self.showRealSize()
                if(action is self.menuZoomInAction):
                    self.zoom(1.2)
                if(action is self.menuZoomOutAction):
                    self.zoom(0.8)
