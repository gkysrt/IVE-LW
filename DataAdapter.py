import PySide2.QtGui as QtGui
import PySide2.QtCore as QtCore
import ImageFile
import os
import datetime

class DataAdapter(QtCore.QObject):

    def __init__(self):
        super(DataAdapter, self).__init__()

    def convert(self, jsonData):
        objectList = []
        for obj in jsonData:
            file = ImageFile.ImageFile(obj['directory'], obj['fileName'], obj['extension'], obj['size'], obj['resolution'], obj['date'], obj['tag'])
            objectList.append(file)

        return objectList