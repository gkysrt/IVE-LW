import PySide2.QtCore as QtCore

class ProxyModel(QtCore.QSortFilterProxyModel):
    def __init__(self, parent = None):
        super(ProxyModel, self).__init__(parent)
        self.setFilterKeyColumn(0)

    #Returns true if index named left is lower than index named right
    def lessThan(self, left, right):
        #Name column
        if(left.column() == 0 and right.column() == 0):
            return left.data().upper() < right.data().upper()

        #Size column
        elif(left.column() == 1 and right.column() == 1):
            return int(left.data()) < int(right.data())

        #Date Column
        elif(left.column() == 2 and right.column() == 2):
            return left.data() < right.data()

        #Resolution column
        elif(left.column() == 3 and right.column() == 3):
            leftSize = left.data().split('x')
            rightSize = right.data().split('x')
            return int(leftSize[0]) * int(leftSize[1]) < int(rightSize[0]) * int(rightSize[1])

        #Tags column
        elif(left.column() == 4 and right.column() == 4):
            return left.data() < right.data()

        else:
            return super(ProxyModel, self).lessThan(left, right)

    #Returns true if item should be included in the model
    #Parameters: int sourceRow, QModelIndex sourceParent
    #Return: bool
    def filterAcceptsRow(self, sourceRow, sourceParent):
        #Implemented searchModel rather than this function
        pass
        return super().filterAcceptsRow(sourceRow, sourceParent)


    #Searches and updates the model
    def searchModel(self, text):
        self.setFilterRegExp(QtCore.QRegExp(text, QtCore.Qt.CaseInsensitive, QtCore.QRegExp.FixedString))
