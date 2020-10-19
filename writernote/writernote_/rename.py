import sys, json

from PyQt5 import QtWidgets

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

class Rename(QtWidgets.QDialog):
    def __init__(self,parent:object = None, copybook:str = None):
        QtWidgets.QDialog.__init__(self, parent)
        self.copybook = copybook

        self.parent = parent
         
         
        textTitle, okPressed = QtWidgets.QInputDialog.getText(None,
                                                        "Get text",
                                                        "Title:",
                                                        QtWidgets.QLineEdit.Normal,
                                                        "")

        if not okPressed: return False
        if textTitle == '': return False
        if self.copybook == textTitle: return False

        posizione = self.parent.indice['titolo'].index(self.copybook)
        self.parent.indice[posizione] = textTitle
        
        # update the window
        self.parent.updateList_()

        # need to save the file
        return self.parent._save_to_path()
