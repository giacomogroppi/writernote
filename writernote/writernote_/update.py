import sys, json
from PyQt5 import QtWidgets

import base64

from PyQt5 import QtGui, QtCore
from PyQt5.Qt import QUrl, QDesktopServices
from PyQt5.QtCore import Qt

class updateWriternote(QtWidgets.QDialog):
    def __init__(self,parent:object = None):
        QtWidgets.QDialog.__init__(self, parent)

        self.parent = parent

        self.ui()
        
    def ui(self) -> bool:
        if self.parent.system == 'linux': 
            ''' aggiornamenti vanno gestiti con snapcraft '''
            return True

        numeroVersione = checkUpdate()
        if numeroVersione == 0:
            return True
        
        check_ = QtWidgets.QMessageBox.question(self,
                "Update",
                "There are " + numeroVersione + " new updates for writernote, do I update?\nDo you want to open browser?",
                QtWidgets.QMessageBox.Open | QtWidgets.QMessageBox.No
                )

        if check_ == QtWidgets.QMessageBox.Yes:
            return self.openbrowser()
            
        else:
            return True

    def openbrowser(self) -> object:
        ''' get latest version of github '''
        url = QUrl("https://github.com/giacomogroppi/writernote/releases/latest")
        return QDesktopServices.openUrl(url)

def decode(versione: str) -> int:
    ''' prende una versione tipo 0.2.3 [current] e restituisce 23 
    version of github:str -> return int '''
    versione = versione.split(".")
    versione2 = 0

    for i, x in enumerate(reversed(versione)):
        versione2 += i*10 + int(x)

    return versione2

def decodeGit(testo: dict):
    if not isinstance(testo, dict):
        if isinstance(testo, str):
            testo = json.loads(testo)


    base64_bytes = testo['content'].encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    testo = message_bytes.decode('ascii')
    
    return testo

def checkUpdate() -> int:
    # necessary for the testing
    #test = {"name":"config.json","path":"writernote/config.json","sha":"ca85f886934ebdb9be2b2b7fc6b28b359feb394d","size":26,"url":"https://api.github.com/repos/giacomogroppi/writernote/contents/writernote/config.json?ref=master","html_url":"https://github.com/giacomogroppi/writernote/blob/master/writernote/config.json","git_url":"https://api.github.com/repos/giacomogroppi/writernote/git/blobs/ca85f886934ebdb9be2b2b7fc6b28b359feb394d","download_url":"https://raw.githubusercontent.com/giacomogroppi/writernote/master/writernote/config.json","type":"file","content":"ewogICAgImF1ZGlvX2NodW5uZWwiOiAxCn0=\n","encoding":"base64","_links":{"self":"https://api.github.com/repos/giacomogroppi/writernote/contents/writernote/config.json?ref=master","git":"https://api.github.com/repos/giacomogroppi/writernote/git/blobs/ca85f886934ebdb9be2b2b7fc6b28b359feb394d","html":"https://github.com/giacomogroppi/writernote/blob/master/writernote/config.json"}}
    
    ''' check the update '''

    import requests
    r = requests.get('https://api.github.com/repos/giacomogroppi/writernote/contents/writernote/config.json')
    
    try:
        with open("config.json") as default:
            config = json.load(default)
    except FileNotFoundError:
        ''' snapcraft PATH '''
        path_ = QtCore.__file__.split("/")
        path_ = path_[1:len(path_)-6]

        path = '/'
        for x in path_:
            path += x + "/"

        try:
            with open(path + "images/default_file.json") as default:
                fileDaScrivere = json.load(default)
                fileDaScrivere['audio_position_path'] = None
        except:
            # ancora da definire per windows
            with open("default_file.json") as default:
                fileDaScrivere = json.load(default)
                fileDaScrivere['audio_position_path'] = None

    versione = decode(config['version'])

    if r.status_code == 403:
        ''' errore da parte del server '''
        return 0

    r = decodeGit(r.text)
    
    versioneGit = r['version'] 
    versioneGit = decode(versioneGit)

    if versioneGit > versione:
        # c'è una nuova versione
        return versioneGit - versione
    
    else:
        return 0 

if __name__ == "__main__":
    checkUpdate()