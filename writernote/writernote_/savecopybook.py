import sys, json

from PyQt5 import QtWidgets

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt

class savecopybook(QtWidgets.QDialog):
    def __init__(self,parent:object = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent
        
        self.ui()
        
    def ui(self) -> bool:
        if self.parent.currentTitle is None:
            # vuol dire che non c'è nulla da salvare
            return True

        posizioneIndex = self.parent.indice['file']['titolo'].index(self.parent.currentTitle)
        fileDaSalvarePath = self.parent.indice['file']['file_testo'][posizioneIndex]

        check_ = QtWidgets.QMessageBox.question(self,
                "Save" + self.parent.currentTitle,
                "If you change the copybook the current Title were be saved\nDo you want to save?",
                QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
                )

        if check_ == QtWidgets.QMessageBox.Discard:
            ''' it means that the user has decided not to save '''
            return True

        elif check_ == QtWidgets.QMessageBox.Save:
            print("save")
            """ Salvataggio del file corrente """
            if self.parent.system == 'linux':
                path = "/tmp/writernote/" + self.parent.temp_ + "/" + fileDaSalvarePath + ".json"

            elif self.parent.system == 'windows':
                path = "C:\\Users\\" + self.parent.username + "\\AppData\\Local\\Temp\\writernote\\" + self.parent.temp_ + "\\" + fileDaSalvarePath + ".json"
                
            # funzione che deve gestire il fatto che l'utente abbia inserito altro testo

            if self.parent.currentTitleJSON['se_registrato']:
                checkSaveIfRegistrato = QtWidgets.QMessageBox.question(self,
                        "Save" + self.parent.currentTitle,
                        "the application is not yet able to save the text you wrote after registering, so I suggest you paste it into another notebook\nDo you want to continue?",
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                        )
                
                if checkSaveIfRegistrato == QtWidgets.QMessageBox.No:
                    ''' in questo caso non deve fare niente '''
                    return False
            
            self.parent.currentTitleJSON['testi'] = [self.parent.editor.toPlainText()]

            with open(path, "w") as f:
                json.dump(self.parent.currentTitleJSON, f)

            return True

        if check_ == QtWidgets.QMessageBox.Discard:
            ''' it means that the user has cleared the window  '''
            return False