#DataAccess.py
#-------------------
#Scans the contents of test folder file and stores items names in a list
#Some file operations including changing directory, scanning files, removing files is done here
#Passes generated data to DataModel.py
#-------------------
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import glob
import os
import json
import datetime
import FormatEnum as imgFormat

class DataAccess(QtCore.QObject):
    scan = QtCore.Signal() #Signal for executing _scan() function
    scanList = QtCore.Signal(list)
    saveList = QtCore.Signal(str, list)
    loadList = QtCore.Signal(str)
    fileCreated = QtCore.Signal(list, int)

    def __init__(self):
        super(DataAccess,self).__init__()
        self.__directory = "/home/gomez/CaveDev/IveLW/test/FolderTest"  # Although it is changable this is the default directory
        self.__imageReader = QtGui.QImageReader()

    def setDirectory(self, newDirectory):   #Setter new working directory
        if (os.path.exists(newDirectory)):
            self.__directory = newDirectory
        else:
            return False

    def directory(self):
        return self.__directory

    def _scanList(self, files):
        print(QtCore.QThread.currentThread().objectName())
        fileCount = len(files)
        fileData = []
        i = 0
        for path in files:
            self.__imageReader.setFileName(path)
            fileName, extension = os.path.splitext(path)
            resolution = self.__imageReader.size()

            jsonObj = {"fileName": os.path.basename(fileName), "extension": extension, "directory": os.path.dirname(path), "size": str(os.path.getsize(path)), "resolution": str(resolution.width()) + " x " + str(resolution.height()), "date": str(datetime.datetime.fromtimestamp(os.path.getctime(path)).date()), "tag":None}
            fileData.append(jsonObj)
            i += 1
            #Returns back the fileData that is read to mainthread 10 by 10
            if((i % 10 == 0) or (fileCount == i)):
                self.fileCreated.emit(fileData, i/fileCount*100)
                fileData = list()

    def _scanCWD(self): #In current working directory, returns all information of the files of supported format in a list of dicts
        try:
            files = list()
            for formats in imgFormat.Format:  #Scan every format type
                files.extend(glob.glob(self.__directory + "/*" + formats.value))

            i = 0
            fileCount = len(files)
            fileData = []
            for path in files:
                self.__imageReader.setFileName(path)
                fileName, extension = os.path.splitext(path)
                resolution = self.__imageReader.size()

                jsonObj = {"fileName": os.path.basename(fileName), "extension": extension, "directory": os.path.dirname(path), "size": str(os.path.getsize(path)), "resolution": str(resolution.width()) + " x " + str(resolution.height()), "date": str(datetime.datetime.fromtimestamp(os.path.getctime(path)).date()), "tag":None}
                fileData.append(jsonObj)
                i += 1
                #Returns back the fileData that is read to mainthread 10 by 10
                if((i % 10 == 0) or (fileCount == i)):
                    self.fileCreated.emit(fileData, i/fileCount*100)
                    fileData = list()

        except NotADirectoryError:
            print("No such directory")

    #Save the current list into a file in json format
    def _saveList(self, fileName, imageList):
        if(os.path.isdir(os.path.dirname(fileName))):
            jsonList = []
            for imageObject in imageList:
                jsonList.append({"fileName": imageObject.fileName(), "extension":imageObject.extension(), "directory":imageObject.directory(), "size":imageObject.size(), "resolution":imageObject.resolution(), "date":str(imageObject.date()), "tag":imageObject.tag()})
            fileName = fileName + ".ive"
            file = open(fileName, "w")
            json.dump(jsonList, file)

    #Loads a list that is saved earlier and returns it
    def _loadList(self, fileName):
        file = open(fileName, "r")
        jsonList = json.load(file)
        fileCount = len(jsonList)
        for i in range(jsonList):
            if((i % 10 == 0) or ((i == fileCount % 10) and fileCount - i < 10)):
                self.fileCreated.emit(jsonList, 100)

    #Delete a image from the disk
    def deleteImage(self, imageName):
        try:
            os.remove(self.__directory+ "/" + imageName)
        except FileNotFoundError:
            print ("File couldn't be found")