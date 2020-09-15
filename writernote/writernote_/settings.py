import os
import sys
import json

from PyQt5 import QtMultimedia
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5 import QtCore, QtGui, QtWidgets


class System:
    def __init__(self):
        self.sistema = sys.platform
        self.Posizione()

    def Posizione(self):
        if self.sistema.upper() == 'linux'.upper(): self.posizione = "/home/giacomo/appgroppi/writernote/mediawriter"
        if self.sistema.upper() == 'linux'.upper(): self.posizione = os.getcwd()
        
    def PozioneConfig(self):
        with open(self.posizione + "/" + "config.json") as f:
            self.config = json.load(f)
        return self.config

    def ImagesPosition(self):
        return self.posizione + "/images"


class Ui_self(QtWidgets.QMainWindow):
    ''' ui for the window '''
    def __init__(self):
        super(Ui_self, self).__init__()

        



def launch():
    print("ciao")
    import sys
    qapp = QtWidgets.QApplication(sys.argv) 
    
    if len(sys.argv) > 1:
        import os
        try:
            path, namefile = os.path.basename(sys.argv[1])
        except ValueError:
            namefile = os.path.basename(sys.argv[1])
            path = os.getcwd()
        
   
        app = Ui_self(path = path, nameFile = namefile)
    else:
        app = Ui_self()
    
    app.show()
    sys.exit(qapp.exec_())

if __name__ == '__main__':
    launch()