import PySide2.QtWidgets as QtWidgets
import PySide2.QtCore as QtCore
import PySide2.QtGui as QtGui
import sys
from Display import *



def main():

	print ("ESC to exit")
	print ("Left-Click on list items displays image in buffer A")
	print ("Ctrl+Left-Click on list opens and displays image in buffer A, in a new tab")
	print ("Middle-Click on list items opens image in a new tab")
	print ("Middle-Click on tabs to close them")
	print ("F to view images on fullscreen")
	print ("Left and Right arrow keys to navigate")
	print ("Press W to open/close fit in view mode")
	print ("Press Q to 100% size image")
	print ("Press Spacebar to see Buffer View")
	print ("Press \tR to see R-channel\n\tG to see G-channel\n\tB to see B-channel\n\tH to see grayscaled" +
		   "\n\tC to see colored")
	print ("QTableView items draggable amongst themselves and over buffers.. " +
		   "Buffers and QTableView accept drops of image files from external sources")
	print ("Press S to open Splitter View, Shift+S to open it on the center of the screen.. " +
		   "Shift modifier also makes the splitter rotate in 45 degree periods")
	print ("Click & Drag mouse middle button to move splitter")
	print ("Shift + Right-Click on image to examine pixel")
	print ("Shortcuts: \n Ctrl+O -> Open Directory \n Ctrl+I -> Open Image \n Ctrl+S -> Save List \n " +
		   "Ctrl+L -> Load List \n Ctrl+D -> Remove Selected File \n Ctrl+T -> Open New Tab \n " +
		   "Ctrl+W -> Close Current Tab \n Ctrl+Tab -> Next Tab \n Ctrl+F -> Open Searchbox")

	app = QtWidgets.QApplication( sys.argv )
	app.setOrganizationName( "CaveVFX" )
	app.setOrganizationDomain( "cavevfx.com" )
	app.setApplicationName( "Ive" )

	mainWindow = Display(app.screens())
	mainWindow.show()

	res = app.exec_()
	sys.exit(res)






main()