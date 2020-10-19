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
        if self.parent.play_: return self.parent.dialog_critical("You can't modify the name right now")
        if self.parent.registrazione_: return self.parent.dialog_critical("You can't change the name of the copybook while you are recording")

        posizione = self.parent.indice['file']['titolo'].index(self.copybook)
        
        self.parent.indice['file'][posizione] = textTitle
        
        # update the window
        return self.parent.updateList_()
