#DataModel.py
#-------------------
#Model class for the IveLW, stores data elements and manages them.
#Stores info about program's state
#-------------------
import PySide2.QtCore as QtCore
import json
import PySide2.QtGui as QtGui
import os, datetime
from ImageFile import ImageFile
import FormatEnum

__all__ = ['DataModel']

class DataModel(QtCore.QAbstractTableModel):

    def __init__(self, parent = None):
        super(DataModel, self).__init__(parent)
        self.__displayedList = list()                       #Image directory list

    def setDisplayedList(self, newList):
        self.beginResetModel()
        self.__displayedList = newList
        self.endResetModel()

    #If an index is given returns specified image object
    def displayedList(self, index = None):
        if(index is not None):
            return self.__displayedList[index]

        return self.__displayedList
    
    def clearModel(self):
        self.beginResetModel()
        self.__displayedList = list()
        self.endResetModel()

    #Change working directory
    def changeDirectory(self, directory):   #Change directory, fetch data and signal reset model
        self.beginResetModel()
        self.dataStream.setDirectory(directory)
        self.attachStream()
        self.endResetModel()

    def addTag(self, tag, index):
        self.__displayedList[index.row()].addTag(tag)

    def clearTag(self, index):
        self.__displayedList[index.row()].clearTagList()

    #Adds an image to the list using a certain filePath
    def addImage(self, imageList):
        self.beginInsertRows(QtCore.QModelIndex(), len (self.__displayedList), len(self.__displayedList) + len(imageList) - 1)
        for image in imageList:
            self.__displayedList.append(image)
        self.endInsertRows()

    #Removes image info from __displayedList
    def removeImage(self, imageIndex):
        #Given a random invalid index since parent is an invalid index
        self.beginRemoveRows(QtCore.QModelIndex(), imageIndex,imageIndex)
        self.__displayedList.pop(imageIndex)
        self.endRemoveRows()

    #Return row count
    def rowCount(self, column = QtCore.QModelIndex()):
        return (len(self.__displayedList))

    def columnCount(self, row = QtCore.QModelIndex()):
        return 6
    #Override QAbstractListModel functions - data()
    def data(self, index, role = QtCore.Qt.DisplayRole):
        row = index.row()
        column = index.column()
        if (role == QtCore.Qt.DisplayRole):
            if(column == 0):
                return self.__displayedList[row].fileName() + self.__displayedList[row].extension()

            elif(column == 1):
                return self.__displayedList[row].size()

            elif(column == 2):
                return self.__displayedList[row].date()

            elif(column == 3):
                return self.__displayedList[row].resolution()

            elif(column == 4):
                return self.__displayedList[row].directory()

            elif(column == 5):
                tags = self.__displayedList[row].tag()
                if(tags is None or len(tags) == 0):
                    return "-"
                else:
                    return ','.join(tags)

        if (role == QtCore.Qt.UserRole):
            return self.__displayedList[row]

    def headerData(self, section, orientation, role):
        if(orientation is QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole):
            if(section == 0):
                return "Image"
            if(section == 1):
                return "Size"
            if(section == 2):
                return "Date"
            if(section == 3):
                return "Resolution"
            if(section == 4):
                return "Directory"
            if(section == 5):
                return "Tags"

        elif(orientation is QtCore.Qt.Horizontal and role == QtCore.Qt.FontRole):
            return QtGui.QFont("Arial")
        else:
            return super().headerData(section,orientation,role)

    #Override supportedDropActions, MoveAction and CopyAction(soon to be) supported
    def supportedDropActions(self):
        return QtCore.Qt.MoveAction | QtCore.Qt.CopyAction

    #Reorganize data after a drag drop operation inside listView
    def reOrganizeData(self, draggedItemIndex, droppedItemIndex):
        #Qt forbids drag&drop operation with from source to source+1 index
        if(draggedItemIndex.row() + 1 != droppedItemIndex.row()):
            self.beginMoveRows(draggedItemIndex.parent(), draggedItemIndex.row(), draggedItemIndex.row(), droppedItemIndex.parent(), droppedItemIndex.row())
            self.__displayedList.insert(droppedItemIndex.row(), self.__displayedList.pop(draggedItemIndex.row()))
            self.endMoveRows()

        #If an item is dropped onto its next row, that item is removed and inserted into the list manually to fix drag&drop problem
        else:
            self.beginRemoveRows(draggedItemIndex.parent(), draggedItemIndex.row(), draggedItemIndex.row() + 1)
            removedItem = self.__displayedList.pop(draggedItemIndex.row())
            self.endRemoveRows()
            self.beginInsertRows(droppedItemIndex.parent(), droppedItemIndex.row() - 1, droppedItemIndex.row())
            self.__displayedList.insert(droppedItemIndex.row(), removedItem)
            self.endInsertRows()

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsDragEnabled | QtCore.Qt.ItemIsDropEnabled | QtCore.Qt.ItemIsEnabled

    def mimeTypes(self):
        return ["object", "path"]

    def mimeData(self, indexes):
        mimeData = QtCore.QMimeData()
        datas = list()
        for index in indexes:
            datas.append(index)

        mimeData.setData(self.mimeTypes()[0], datas)
        print("ko")
        return mimeData

    def canDropMimeData(self, data, action, row, column, parent):
        if(data.hasUrls()):
            supportedExtensions = set()
            for imageFormat in FormatEnum.Format:
                supportedExtensions.add(imageFormat.value)

            for url in data.urls():
                fileName, extension = os.path.splitext(url.path())
                if(extension in supportedExtensions):
                    return True
        return False

    #TODO: need to find a better way for dropMimeData()
    def dropMimeData(self, data, action, row, column, parent):
        if(self.canDropMimeData(data, action, row, column, parent)):
            self.beginInsertRows(parent, row, row + len(data.urls()))
            imageReader = QtGui.QImageReader()
            i = 0
            for url in data.urls():
                fileName, extension = os.path.splitext(url.path())
                imageReader.setFileName(url.path())
                resolution = imageReader.size()
                self.__displayedList.insert(row + i, ImageFile(os.path.dirname(url.path()), os.path.basename(fileName), extension, str(os.path.getsize(url.path())), str(resolution.width()) + " x " + str(resolution.height()), datetime.datetime.fromtimestamp(os.path.getctime(url.path())).date()))
                i += 1

            self.endInsertRows()

        return super(DataModel, self).dropMimeData(data, action, row, column, parent)

