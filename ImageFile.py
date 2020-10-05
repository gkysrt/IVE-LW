import PySide2.QtGui as QtGui
class ImageFile(object):
    def __init__(self, directory = None, fileName = None, extension = None, size = None, resolution = None, date = None, tag = None):
        super(ImageFile, self).__init__()
        self.__directory = directory
        self.__fileName = fileName
        self.__extension = extension
        self.__path = directory + "/" + fileName + extension
        self.__size = size
        self.__resolution = resolution
        self.__date = str(date)
        self.__tagList = list()
        if(tag is not None):
            self.__tagList = tag

    def resolution(self):
        return self.__resolution

    def imageFormat(self):
        return self.imageReader.format()

    def setFileName(self, fileName):
        self.__fileName = fileName

    def setDirectory(self, directory):
        self.__directory = directory

    def setExtension(self, extension):
        self.__extension = extension

    def setPath(self, path):
        self.__path = path

    def setSize(self, size):
        self.__size = size

    def setDate(self, date):
        self.__date = str(date)

    def setTagList(self, tag):
        self.__tagList = tag

    def clearTagList(self):
        self.__tagList = list()

    def addTag(self, tag):
        self.__tagList.append(tag)

    def fileName(self):
        return self.__fileName

    def directory(self):
        return self.__directory

    def extension(self):
        return self.__extension

    def path(self):
        return self.__path

    def size(self):
        return self.__size

    def date(self):
        return self.__date

    def tag(self):
        return self.__tagList