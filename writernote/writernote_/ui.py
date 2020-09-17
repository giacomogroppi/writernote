#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os

import json

import threading, subprocess, multiprocessing

import sys
import traceback

from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave

from writernote_ import zip_
import shutil
from writernote_ import audio_decoder, audioRecoder


#if not os.getcwd() == '/home/giacomo/appgroppi/writernote/writernote':
#    os.system("$PATH")
#    os.system("ls $SNAP/lib/python3.6/site-packages")
#    sys.path.append(os.path.realpath("$SNAP/lib/python3.6/site-packages"))

    
from PyQt5 import QtCore 

from PyQt5 import QtMultimedia
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *


class Ui_self(QtWidgets.QMainWindow):
    def __init__(self, path = None, nameFile = None):
        super(Ui_self, self).__init__()

        self.path = path
        self.temp_ = None 
        self.nameFile = nameFile
        self.controlloScrittura = False
        self.precedente_ = ''
        self.currentTitle = None
        self.registrazione_ = False
        self.currentTime = 0
        self.play_ = False

        self.setupUi()
        
        if self.path is not None and self.nameFile is not None:
            self.file_open(True)


    def setupUi(self):   
        self.path = None
        self.caricamentoJSON()

        self.setEnabled_()
        
        QtCore.QMetaObject.connectSlotsByName(self)

        self.createTempFolder_()
        

    def cambiamenti_testo(self):
        """ Funzione che viene richiamata tutte le volte che durante qualcosa viene scritto qualcosa """
        #text = self.editor.toPlainText()[-1:]
        
        # tutte le volte salva tutto il codice in html, in modo da non perdere i tag
        text = self.editor.toHtml()

        if self.registrazione_:
            self.currentTitleJSON['testi'].append(text)
            self.currentTitleJSON['posizione_iniz'].append(str(int(time.time()) - self.tempoAudioRegistazione))
            self.currentFile = 0
        

    def cambiamenti_selezione(self):
        if  self.controlloScrittura:
            """ it means the user is not writing """
            text = self.editor.textCursor().selectedText()
            position = self.editor.textCursor().selectionStart()
            print(text)


    def closeEvent(self, event):
        if self.play_:
            self.player.stop()
            self.event_stop.set()

        if self.path is None or self.path == '':
            self.path = os.getcwd()


        try:
            with open("indice.json") as indice:
                indice_base = json.load(indice)
        except FileNotFoundError:
            ''' snapcraft PATH '''
            path_ = QtCore.__file__.split("/")
            path_ = path_[1:len(path_)-6]

            path = '/'
            for x in path_: 
                path += x + "/"

            with open(path + "images/indice.json") as indice:
                indice_base = json.load(indice)

        if indice_base == self.indice:
            # It means there is no file to save
            import shutil
            shutil.rmtree(self.path + "/" + self.temp_)
            
            return True

        close = QtWidgets.QMessageBox.question(self,
                                     "QUIT",
                                     "Do you want to save?",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.No
                                     )

        import shutil
        if close == QtWidgets.QMessageBox.Yes:
            print("SI")
            if self.nameFile is not None:
                if not zip_.compressFolder(self.path, self.temp_, self.nameFile):
                    self.dialog_critical("We had a problem to save the save.\nPlease retry")
                    event.ignore()
                    return False
            else:
                if not self.file_save():
                    event.ignore()
                else:
                    event.accept()

                return False       
            
            shutil.rmtree(self.path + "/" + self.temp_)    
            
            event.accept()
        
        elif close == QtWidgets.QMessageBox.No:
            shutil.rmtree(self.path + "/" + self.temp_)
            event.accept()
            return False

        else: 
            event.ignore()
            return False



    def newCopyBook(self):
        textTitle, okPressed = QtWidgets.QInputDialog.getText(None, 
                                                        "Get text",
                                                        "Title:", 
                                                        QtWidgets.QLineEdit.Normal, 
                                                        "")   
        
        if not okPressed: return

        if textTitle != '':
            # ui.lineedit.setText(text)
            self.newCopyBook_(textTitle)
            
        else: 
            self.dialog_critical("You need to insert something")
            return

        self.deleteCopyBook.setEnabled(True)
        

    def deleteAudio_Function(self, currentItem = None):
        if currentItem is None:
            currentItem == self.currentTitle

        check_ = QtWidgets.QMessageBox.question(
                                self,
                                "Delete audio",
                                "Do you want to delete the audio, the file will be saved",
                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
                                )

        if check_ == QtWidgets.QMessageBox.No:
            return False

        posizione = self.indice['file']['titolo'].index(currentItem.text())
        
        ### Rimozione dell'audio
        os.remove(self.path + "/" + self.temp_ + "/" + self.indice['file']['audio'][posizione])
        
        with open(self.path + "/" + self.temp_ + "/" + self.indice['file']['file_testo'][posizione]) as fileReadable:
            fileReadable = json.load(fileReadable)
            fileReadable['audio_position_path'] = None

            with open(self.path + "/" + self.temp_ + "/" + self.indice['file']['file_testo'][posizione], "w") as file_:
                ### file.write(str(fileReadable).replace("False", "false").replace("None", "null"))
                json.dump(fileReadable, file_)

        self.indice['file']['audio'][posizione] = None

        self.updateList_()

    def aggiornoTextEditor(self):
        """
            deve aggiungere nella parte
        """
        self.currentTimeLabel = QtWidgets.QLabel(self)
        self.currentTimeLabel.setMinimumSize(QtCore.QSize(80, 0))
        self.currentTimeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.currentTimeLabel.setObjectName("currentTimeLabel")

        
        self.layout_table = QtWidgets.QVBoxLayout()

        #self.layout.addWidget(self.currentTimeLabel, 1, 1)
        #self.layout.addWidget(self.timeSlider, 1, 1)

        global listwidget 
        listwidget = self.listwidget


    def on_clickMenuList(self):
        """ Funzione per gestire il SINGOLO click all'interno del menu """
        print("on_clickMenuList")
        c = True
        if self.currentTitle is not None:
            posizione = self.indice['file']['titolo'].index(self.currentTitle)
        else:
            c = False
            posizione = 0

        fileDaSalvare = self.indice['file']['file_testo'][posizione]

        if c:
            ''' richiesta all'utente se vuole salvare il file '''
            check_ = QtWidgets.QMessageBox.question(self,
                "Save" + self.currentTitle, 
                "If you change the copybook the current Title were be saved\nDo you want to continue?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel
                )


            if check_ == QtWidgets.QMessageBox.Cancel:
                return False
            
            elif check_ == QtWidgets.QMessageBox.Yes:
                """ Salvataggio del file corrente """
                with open(self.path + "/" + self.temp_ + "/" + fileDaSalvare + ".json", "w") as f:
                    json.dump(self.currentTitleJSON, f)
        
        # Change the current title
        self.currentTitle = self.listwidget.currentItem().text()
        self.update_title()

        """ Load per il file nuovo """
        posizione = self.indice['file']['titolo'].index(self.currentTitle)
        fileDaCaricare = self.indice['file']['file_testo'][posizione]

        with open(self.path + "/" + self.temp_ + "/" + fileDaCaricare + ".json") as fileD:
            self.currentTitleJSON = json.load(fileD)

        # caricamento del testo
        if not self.indice['file']['audio'][posizione] and len(self.currentTitleJSON['testi']) != 0:
            # se non è registrato
            self.editor.setHtml(self.currentTitleJSON['testi'][0])
            
        elif self.indice['file']['audio'][posizione]:
            ''' vecchio formato '''
            ##daCaricare_ = ''
            ##for x in self.currentTitleJSON['testi']:
            ##    daCaricare_ += x

            ''' nuovo formato '''
            daCaricare_ = self.currentTitleJSON['testi'][-1]

            self.editor.setHtml(daCaricare_)
        else:
            print("on_clickmenulist else")
            self.editor.setHtml('')
        
        if self.currentTitleJSON['se_tradotto']: print("tradotto")

        try:
            posizione = self.indice['file']['titolo'].index(self.currentTitle)
        except:
            return True

        self.editor.setEnabled(True)
        self.deleteCopyBook.setEnabled(True)
        if self.indice['file']['audio'][posizione] is None:
            # se non c'è l'audio
            self.volumeSlider.setEnabled(False)
            self.registrare_action.setEnabled(False)
            self.registrare_actionStop.setEnabled(False)
            self.video_import.setEnabled(False)
            self.riascoltoAudio.setEnabled(False)
            self.deleteAudio_Button.setEnabled(False)
            
            return True

        self.volumeSlider.setEnabled(True)
        self.registrare_actionStop.setDisabled(True)
        self.registrare_action.setDisabled(True)
        self.video_import.setDisabled(True)

        if not self.currentTitleJSON['se_tradotto']: self.convertAudio.setEnabled(True)
        self.riascoltoAudio.setEnabled(True)
        self.deleteAudio_Button.setEnabled(True)
        
        if self.currentTitleJSON['testi']:
            """ if it is empty """
            self.print_action.setDisabled(True)

        self.player.setMedia(
                QMediaContent(
                    QUrl.fromLocalFile(self.path + "/" + self.temp_ + "/" + self.indice['file']['audio'][posizione])
                )
            )
        
        

    def updateList_(self):
        self.indice['video_checksum'] = len(self.indice['file']['titolo'])

        """ Aggiornamento della lista """
        self.listwidget.clear()



        for i, x_ in enumerate(self.indice['file']['titolo']):
            if x_ is not None:
                self.listwidget.insertItem(i, x_)

            else:
                self.listwidget.insertItem(i, "No title")

        
        
        with open(self.path + "/" + self.temp_ + "/indice.json", "w") as fileD:
            json.dump(self.indice, fileD)




    def riascolto_Audio(self):
        """ Funzione del self che permette di riascoltare l'audio del copybook """
        # posizione = self.indice['file']['titolo'].index(self.currentTitle)
        if self.play_: 
            ## he need to stop:
            self.editor.setEnabled(True)
            self.deleteAudio_Button.setEnabled(True)

            self.player.stop()
            self.play_ = False
            return
        
        self.player.play()

        self.play_ = True

        self.pauseButton.setEnabled(True)
        
        print("riascolto_Audio -> finished") 
        



    def compressVideo(self, currentItem):
        """ It compress the video in the saim folder """
        position = self.indice['file']['titolo'].index(currentItem.text())
        
        ### for i, x in enumerate(self.titolo):
        ###     if x == currentItem.text():
        ###         position = i
        ###         break


        if self.indice['file']['compressione'][position]:
            self.dialog_critical("The video is already compress in h264")

        else:
            if not os.path.exists(self.indice['file']['video'][position]):

                self.dialog_critical("The video didn't exist or you have move it")

            else:
                path_file = self.indice['file']['video'][position]

                path_file_nameTo = path_file.split('.')

                comando = 'ffmpeg -i ' + path_file +' -c:v libx264 -c:a copy -x265-params crf=20  ' + path_file[:-len(path_file_nameTo[len(path_file_nameTo)-1])-1] + ".mp4"
                comando.split(' ')

                self.dialog_critical("It will take some time to compress the video")
                self.compressione_ = subprocess.Popen(comando)

    def contextMenuEvent(self, event):
        ### Funzione per gestire il tasto destro all'interno del menu del copybook
        
        if not os.path.exists(self.path + "/" + self.temp_ + "/indice.json"):
            return 


        contextMenu = QMenu(self.listwidget)

        self.listwidget.addQuaderno = contextMenu.addAction("New")
        self.listwidget.deleteQuaderno = contextMenu.addAction("Del")
        self.listwidget.deleteAudio = contextMenu.addAction("Del audio")
        self.listwidget.comprimiVideo = contextMenu.addAction("Compress Video")
        self.listwidget.convert_textAudio = contextMenu.addAction("Audio -> Text")
        
        

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        currentItem = self.listwidget.currentItem()
        
        if currentItem is None: return

        if action == self.listwidget.addQuaderno:
            self.newCopyBook()
        
        elif action == self.listwidget.deleteQuaderno:
            self.deleteCopyBookFunction(currentItem)
        
        elif action == self.listwidget.deleteAudio:
            self.deleteAudio_Function(currentItem=currentItem)



        elif action == self.listwidget.comprimiVideo:
            
            self.compressVideo(currentItem)

        elif action == self.listwidget.convert_textAudio:
            if self.on_clickMenuList() is True:
                self.convertAudioToText()
        else:
            pass

            

    def convertAudioToText(self, currentItem = None):
        """ He convert the audio into text """
        # for i, x in self.titolo:
        #     if x == currentItem.text():
        #         break

        if currentItem is None:
            try:
                position = self.indice['file']['titolo'].index(currentItem.text())
            except:
                return False
        else:
            position = self.indice['file']['titolo'].index(self.currentTitle)

        if self.indice['file']['audio'] is None: 
            self.dialog_critical("You need to include a video before convert it into text")
            return False

        if self.currentTitleJSON['se_tradotto']:
            self.dialog_critical("You have already translate the audio to text")
            return False


        """ check internet connection with the google dns """
        import socket
        try:
            hostname = 'www.google.com'
            socket.gethostbyname(hostname)
        
        except socket.gaierror:
            self.dialog_critical("You need a connection to internet")
            return False

        #path_spitting = self.indice['file']['audio'][position]

        text = audio_decoder.Video(
            path = self.path,
            temp_ = self.temp_,
            nameAudio = self.indice['file']['audio'][position]
            )
        
        verifica, text_ = text.decoder()
        
        if text_ == '':
            self.dialog_critical("The audio is empty")
            
            self.currentTitleJSON['testi'] = ['']
            self.currentTitleJSON['se_tradotto'] = True
            
            return False

        if not verifica:
            self.dialog_critical("I had a problem in traslating the text\nPlease retry")
            return False

        self.convertAudio.setDisabled(True)
        self.currentTitleJSON['testi'] = [text_]
        self.currentTitleJSON['se_tradotto'] = True
        self.editor.setPlainText(self.currentTitleJSON['testi'][0])
        


    def caricamentoJSON(self):
        try:
            with open("indice.json", 'r') as f:
                self.indice = json.load(f)
        except FileNotFoundError:
            ''' snapcraft PATH '''
            path_ = QtCore.__file__.split("/")
            path_ = path_[1:len(path_)-6]

            path = '/'
            for x in path_: 
                path += x + "/"

            print("PATH:",path)
            with open(path + "images/indice.json") as f:
                self.indice = json.load(f)
                
        except:
            return self.dialog_critical("Sorry we had a internal problem, with the indice.json, retry.")

        return True

    def videoImport(self):
        """
        la funzione viene richiamata all'interno del programma
        per importare un video all'interno del progetto -->
        bisogna che il file sia già salvato
        """
        if self.path == None or self.nameFile is None:
            self.dialog_critical("You need to save the file before continuing")
            return False

        # Serve per capire dove sia il file che vuole scindere
        path_File, _ = QFileDialog.getOpenFileName(self, "Open video", "", "Video (*.mp4);All files (*.*)")

        if path_File:
            if not os.path.exists(path_File):
                self.dialog_critical(str("The file didn't exist"))
                return 0
        _, file_extension = os.path.splitext(path_File)
        
        possibleExtantion = [
            'wmk', 
            'flv', 
            'gif', 
            'avi', 
            'mov',
            'mp4'
            ]

        if not file_extension in possibleExtantion:
            self.dialog_critical("Sorry I can't import the file extantion " + str(file_extension))
            return  

        try: 
            position = self.indice['file']['titolo'].index(self.currentTitle)
        except:
            self.dialog_critical("you need to create a new copybook before add a video")
            return


        video = Video(path_File, self.temp_)
        
        """ Scissione """
        audioName = video.scissione()

        # Salva il nome dell'audio all'interno file audioName --> richiama poi l'aggiornamento dell'indice
        self.indice['file']['audio'][position] = audioName



            
        self.updateList_()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Critical)
        dlg.show()


    def scissionePATH(self, path):
        path = path.split('/')
        
        
        path_finale = ''
        for x in path[:-1]:
            # print(path_finale)
            if x != '': path_finale = path_finale + '/' +  x
        
        # in this case the path change and we need to moove the temp folder
        if self.path != path_finale:
            print(self.path, self.temp_, path_finale)

            shutil.move(self.path + "/" + self.temp_, path_finale + "/")

        self.path = path_finale
        #MyWindow.path = path_finale
        self.nameFile = path[len(path)-1]
        

    def file_open(self, check = False):

        if not check: 
            path, _ = QFileDialog.getOpenFileName(self, "Open file", "", "Writernote file (*.writer);All files (*.*)")
        else:
            path = self.path
        
        if path:
            if not check: self.scissionePATH(path)
            
            if not os.path.exists(self.path + "/" + self.nameFile):
                self.dialog_critical("The file didn't exist")
                return

            if not zip_.extractAll(self.nameFile, self.path, self.temp_):
                # Se l'estrazione ha trovato qualche errore 
                self.dialog_critical("We had some problem to read the file, retry or see the log.")
                return

            # Carica l'indice dalla cartella ./temporaneo
            with open(self.path + "/" + self.temp_ + "/indice.json") as f:
                self.indice = json.load(f)
                

            self.update_title()
            self.updateList_()


            if len(self.indice['file']['titolo']) != len(self.indice['file']['audio']) or len(self.indice['file']['titolo']) != int(self.indice['video_checksum']):
                del self.indice
                self.dialog_critical("The file is curropted")
            
            self.NewAudio.setEnabled(True)
        else:
            return False

    def file_save(self):
        if self.path is None or self.nameFile is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()
        else:
            self._save_to_path()

    def file_saveas(self):
        if self.path is None or self.nameFile is None:
            path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Text documents (*.txt);All files (*.*)")
            
            if not path:
                # If dialog is cancelled, will return False
                return False

        self.scissionePATH(path)
        self._save_to_path()

    def createTempFolder_(self):
        """ Viene eseguita la funzione appena il programma finisce di caricare """
        if self.path is None: self.path = os.getcwd()

        print("self.temp_: ",self.temp_)
        if self.temp_ is not None: return
        
        variabile = 0
        while True:
            #print(self.path + "./temporaneo" + str(variabile))
            if not os.path.exists(self.path + "/.temporaneo" + str(variabile)):
                self.temp_ = '.temporaneo' + str(variabile)
                #MyWindow.temp_ = '.temporaneo' + str(variabile)
                break
            variabile = variabile + 1

        os.mkdir(self.path + "/" + self.temp_)

    
    def NewFileComplite(self):
        """ crea una cartella completa con l'indice vuoto, senza settare il nome del file """
        if self.path is None: self.path = os.getcwd()
    
        if os.path.exists(self.path + "/" + self.temp_ + "/indice.json"):
            self.dialog_critical("You have already create a new book, to write something create a new copybook")
            return

        with open(self.path + "/" + self.temp_ + "/" + "indice.json", "w") as f: 
            f.write(str(self.indice).replace("False", "false").replace("None", "null"))
        
        self.NewAudio.setEnabled(True)

        

    def newCopyBook_(self, callback):
        """ funzione che viene richiamata da newCopyBook """
        if callback == '': return
        
        if callback in self.indice['file']['titolo']: 
            self.dialog_critical("you can't create two different copybook with the same name")
            return

        #self.video.append(None)
        #self.audio.append(None)
        #self.titolo.append(callback)
        #self.compressione.append(None)
        self.indice['file']['video'].append(None)
        self.indice['file']['audio'].append(None)
        self.indice['file']['titolo'].append(callback)
        self.indice['file']['compressione'].append(None)


        self.currentTitle = callback

        import datetime

        i = 0
        nomeTemp = str(datetime.datetime.now()).replace(" ", "").replace(":", "")

        while True:
            if not os.path.exists(self.path + "/" + self.temp_ + "/" + "nameFile" +str(nomeTemp) + str(i)):    
                nomeTemp = "nameFile" +str(nomeTemp) + str(i)
                break
            i += 1

        self.indice['file']['file_testo'].append(nomeTemp)

        try:
            with open("default_file.json") as default:
                fileDaScrivere = json.load(default)
                fileDaScrivere['audio_position_path'] = None 
        except FileNotFoundError:
            ''' snapcraft PATH '''
            path_ = QtCore.__file__.split("/")
            path_ = path_[1:len(path_)-6]

            path = '/'
            for x in path_: 
                path += x + "/"

            with open(path + "images/default_file.json") as default:
                fileDaScrivere = json.load(default)
                fileDaScrivere['audio_position_path'] = None 

        with open(self.path + "/" + self.temp_ + "/" + nomeTemp + ".json", "w") as file_:
            json.dump(fileDaScrivere, file_)

        self.editor.setHtml('')

        del i, nomeTemp
        
        # Carica il json
        self.currentTitleJSON = fileDaScrivere

        self.file_menu.menuAction().setVisible(True)
        self.edit_menu.menuAction().setVisible(True)
        self.Audio_option_menu.menuAction().setVisible(True)

        self.editor.setDisabled(True) # Abilita alla scrittura del file
        self.riascoltoAudio.setDisabled(True)
        self.NewAudio.setDisabled(False)
        self.deleteAudio_Button.setDisabled(True)
        
        self.updateList_()

    def _save_to_path(self):
        if self.nameFile is None:
            self.dialog_critical("Reselct the name of the file please")
            return False

        """ salvataggio degli indici """

        self.indice['video_checksum'] = len(self.indice['file']['titolo'])

        with open(self.path + "/" + self.temp_ + "/indice.json", "w") as f:
            json.dump(self.indice, f)
            ### f.write(str(self.indice))

        if self.currentTitle is not None:
            posizione = self.indice['file']['titolo'].index(self.currentTitle)

            with open(self.path + "/" + self.temp_ + "/" + self.indice['file']['file_testo'][posizione] + ".json", "w") as c: 
                if self.registrazione_:
                    ''' deve stoppare la registrazione '''
                    self.stopRecording()
                else:
                    if not self.currentTitleJSON['se_registrato']:
                        # se non è registrato
                        self.currentTitleJSON['testi'] = [self.editor.toHtml()]
                print("_save_to_path ", self.currentTitleJSON)
                json.dump(self.currentTitleJSON, c)


        if not zip_.compressFolder(self.path, self.temp_, self.nameFile):
            self.dialog_critical("We had a problem, retry or check the log")
            return False
        else:
            return True


    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec_():
            self.editor.print_(dlg.printer())

    def update_title(self):
        if self.nameFile is None:
            name = 'Untitled'
        else:
            nameTemp, _ = os.path.splitext(self.nameFile)
            print(nameTemp)
            name = nameTemp + " - " + 'Writernote' if self.currentTitle is None else nameTemp + " - " + self.currentTitle + " - Writernote"
        self.setWindowTitle(name)

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode( 1 if self.editor.lineWrapMode() == 0 else 0 )


    '''
    definizione di tutte le funzioni necessarie per registrare l'audio
    mentre si scrive

    '''

    def normalize(self, snd_data):
        print(snd_data)
        "Average the volume out"
        MAXIMUM = 16384
        times = float(MAXIMUM)/max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i*times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"
        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i)>self.THRESHOLD:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        silence = [0] * int(seconds * self.RATE)
        r = array('h', silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    @classmethod
    def record(self, in_queue, *arg):
        
        self.path = arg[0]
        self.temp_ = arg[1]
        self.indice = arg[2]
        self.currentTitle = [3]
        
        
        print(self.path)

        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100

        print("record")
        self.audio = pyaudio.PyAudio()
        
        stream = self.audio.open(format=self.FORMAT, channels=1, rate=self.RATE,
            input=True, output=True,
            frames_per_buffer=self.CHUNK_SIZE)

        
        snd_started = False
        
        r = array('h')
        
        while True:

            if not in_queue.empty():
                # if the list is empty  
                if in_queue.get() == 'stop': break
            

            snd_data = array('h', stream.read(self.CHUNK_SIZE))
            if byteorder == 'big':
                snd_data.byteswap()
            r.extend(snd_data)


            
        print("uscito dal ciclo")


        sample_width = self.audio.get_sample_size(self.FORMAT)
        stream.stop_stream()
        stream.close()



        self.audio.terminate()

        r = audioRecoder.normalize(r)
        r = audioRecoder.trim(r)
        
        r = pack('<' + ('h'*len(r)), *r)

        import datetime
        date = str(datetime.datetime.now()).replace(" ", "").replace(":", "")
        i = 0
        while True:
            if not os.path.exists(self.path + "/" + self.temp_ + "/" + "audio" + str(date) + str(i)):
                nameAudioPosition =  "audio" + str(date) + str(i)
                break
            i += 1
        del i

        wf = wave.open(self.path + "/" + self.temp_ + "/" + nameAudioPosition, 'wb')
        
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        
        wf.setframerate(self.RATE)
        wf.writeframes(r)
        wf.close()


        return nameAudioPosition

    def record_to_file(self, method):
        if self.currentTitle is None:
            self.dialog_critical("You need to select a title in the left of the window")
            return
        


        self.THRESHOLD = 500
        self.CHUNK_SIZE = 1024
        self.FORMAT = pyaudio.paInt16
        self.RATE = 44100

        def callBack(item):
            print("callback: ", item)


        if method == 'start': 

            manager = multiprocessing.Manager()
            self.odd_queue = manager.Queue()
            
            self.pool = multiprocessing.Pool()
            
            self.odd_result = self.pool.apply_async(self.record, args=(self.odd_queue, self.path, self.temp_, self.indice, self.currentTitle), error_callback=callBack)
                       
            
        else:
            """ Chiude la registrazione e salva nel path/self.temp_/numerocasuale """ 
            self.odd_queue.put("stop")
            self.pool.close()
            self.pool.join()

            # Riprende l'indice
            nameAudio = self.odd_result.get()
            position = self.indice['file']['titolo'].index(self.currentTitle)
            
            self.indice['file']['audio'][position] = nameAudio

            self.currentTitleJSON['audio_position_path'] = nameAudio
            
            self.updateList_()


    def position_changed(self, position):
        """ Se l'utente manualmente cambia la posizione """
        self.slider.setValue(position*1000)
 
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
    def setPositionSliderTime(self, value):
        ''' gestisce il cambiamento dello slider del tempo '''
        # print("setPositionSliderTime {}".format(value))
        self.player.setPosition(value)

 
    def handle_errors(self):
        self.playBtn.setEnabled(False)
        self.label.setText("Error: " + self.mediaPlayer.errorString())
 
    def playButtonFunction(self):
        print("playButtonFunction -> start")
        if self.play_: return

        self.pauseButton.setEnabled(True)
        self.timeSlider.setEnabled(True)
        self.volumeSlider.setEnabled(True)
        self.playButton.setEnabled(False)

        self.riascolto_Audio()
        self.player.setPosition(self.position)
        
        print("playButtonFunction -> stop")


    def update_position_audio(self, position):
        ''' funzione che gestiste il riascolto dell'audio '''
        h, r = divmod(position, 36000)
        m, r = divmod(r, 60000)
        s, _ = divmod(r, 1000)
        
    
        self.currentTime = int(str(h) + str(m) + str(s) if h else str(m) + str(s))
        
        if self.play_:
            try:
                position = self.currentTitleJSON['posizione_iniz'].index(str(self.currentTime))
            except ValueError:
                ## in caso in cui l'utente in quel secondo dell'audio non abbia detto niente
                return
            
            ''' vecchia struttura dati '''
            #testo = ''
            #for x in self.currentTitleJSON['testi'][:position]:
            #    testo += x

            ''' nuova struttura dati '''
            testo = self.currentTitleJSON['testi'][position]
            
            self.editor.setPlainText(testo)
            
        
        self.timeSlider.blockSignals(True)
        
        if self.player.duration() != 0:
            self.timeSlider.setValue(position/self.player.duration()*100)
        
        self.timeSlider.blockSignals(False)

    def stop_riascolto_audio(self):
        ''' Funzione che gestisce la pausa dell'audio in riproduzione '''
        print("stop_riascolto_audio -> start")
        if not self.play_ : return
        
        self.play_ = False
        self.position = self.player.position()
        self.pauseButton.setDisabled(True)
        self.playButton.setEnabled(True)
        self.timeSlider.setEnabled(False)
        self.volumeSlider.setEnabled(True)
        
        

        self.player.stop()
        self.event_stop.set()
        print("stop_riascolto_audio -> stop")

    def startRecording(self):
        self.tempoAudioRegistazione = int(time.time())
        self.registrazione_ = True
        self.record_to_file('start')
    
    def stopRecording(self):
        self.record_to_file('stop')
        self.registrazione_ = False
        

    def setVolume(self, c):
        self.player.setVolume(c)

    def undo_action(self):
        self.editor.undo()

    def cutFunction(self):
        self.editor.cut()


    def setEnabled_(self):
        if os.path.isdir("images"):
            pathFolder = ''
        else:
            ''' snapcraft PATH '''
            path_ = QtCore.__file__.split("/")
            path_ = path_[1:len(path_)-6]

            pathFolder = '/'
            for x in path_: 
                pathFolder += x + "/"
            del path_

        self.setObjectName("self")
        self.resize(830, 675)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(814, 674))
        self.setSizeIncrement(QtCore.QSize(0, 0))
        self.setFocusPolicy(QtCore.Qt.NoFocus)
        self.setWindowOpacity(1.0)
        self.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.centralWidget = QtWidgets.QWidget(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setFocusPolicy(QtCore.Qt.TabFocus)
        self.centralWidget.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setContentsMargins(8, 8, 8, 8)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        

        # Creazione del QMediaPlayer()
        self.player = QtMultimedia.QMediaPlayer()
        
        self.player.positionChanged.connect(self.update_position_audio)
        

        # Play button
        self.playButton = QtWidgets.QPushButton(self.centralWidget)
        self.playButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(pathFolder + "images/control.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.playButton.setIcon(icon1)
        self.playButton.setObjectName("playButton")
        self.playButton.clicked.connect(self.playButtonFunction)
        self.horizontalLayout_5.addWidget(self.playButton)
        
        ### definizione dell'evento per stoppare il riascolto dell'audio
        self.event_stop = threading.Event()

        self.pauseButton = QtWidgets.QPushButton(self.centralWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(pathFolder + "images/control-pause.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pauseButton.setIcon(icon2)
        self.pauseButton.setObjectName("pauseButton")
        self.horizontalLayout_5.addWidget(self.pauseButton)
        self.pauseButton.clicked.connect(self.stop_riascolto_audio)
        
        # self.stopButton.setObjectName("Stop audio playback")
        self.playButton.setObjectName("Start audio playback")
        self.pauseButton.setObjectName("Pause audio playback")

        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(pathFolder + "images/speaker-volume.png"))
        self.label.setObjectName("label")
        self.horizontalLayout_5.addWidget(self.label)
        self.volumeSlider = QtWidgets.QSlider(self.centralWidget)
        self.volumeSlider.setMaximum(100)
        self.volumeSlider.setProperty("value", 100)
        self.volumeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.volumeSlider.setObjectName("volumeSlider")
        self.horizontalLayout_5.addWidget(self.volumeSlider)
        self.gridLayout.addLayout(self.horizontalLayout_5, 2, 1, 1, 1)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        self.editor = QtWidgets.QTextEdit(self.centralWidget)
        self.editor.setObjectName("textEdit")
        # modificazioni al testo
        self.editor.selectionChanged.connect(self.cambiamenti_selezione)
        self.editor.textChanged.connect(self.cambiamenti_testo)
        
        self.gridLayout.addWidget(self.editor, 0, 1, 1, 1)
        self.editor.setDisabled(True)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.currentTimeLabel = QtWidgets.QLabel(self.centralWidget)
        self.currentTimeLabel.setMinimumSize(QtCore.QSize(30, 0))
        self.currentTimeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.currentTimeLabel.setObjectName("currentTimeLabel")
        self.horizontalLayout_4.addWidget(self.currentTimeLabel)
        self.timeSlider = QtWidgets.QSlider(self.centralWidget)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setObjectName("timeSlider")
        self.horizontalLayout_4.addWidget(self.timeSlider)
        self.totalTimeLabel = QtWidgets.QLabel(self.centralWidget)
        self.totalTimeLabel.setMinimumSize(QtCore.QSize(0, 0))
        self.totalTimeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.totalTimeLabel.setObjectName("totalTimeLabel")
        self.horizontalLayout_4.addWidget(self.totalTimeLabel, 0, QtCore.Qt.AlignBottom)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

                   

        self.timeSlider.valueChanged.connect(self.setPositionSliderTime)
        # self.timeSlider.changeEvent.connect()

        ### ENABLE AUDIO
        self.playButton.setEnabled(False)
        self.pauseButton.setEnabled(False)
        self.timeSlider.setEnabled(False)
        self.volumeSlider.setEnabled(False)



        # Lista per i titoli
        self.listwidget = QtWidgets.QListWidget(self.centralWidget)
        self.listwidget.setEnabled(True)
        self.listwidget.setMaximumSize(QtCore.QSize(100, 16777215))
        self.listwidget.setMouseTracking(False)
        self.listwidget.setObjectName("listWidget")
        
        self.gridLayout.addWidget(self.listwidget, 0, 0, 3, 1)
        self.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

        self.toolBar = QToolBar("File")
        self.toolBar.setIconSize(QSize(20, 20))
        self.toolBar.setObjectName("toolBar")

        self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        self.file_menu = self.menuBar().addMenu("&File")

        new_menu_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'newFileBig.png')), "New File", self)
        new_menu_action.setStatusTip("Create new file on the directory")
        new_menu_action.triggered.connect(self.NewFileComplite)
        self.file_menu.addAction(new_menu_action)
        self.toolBar.addAction(new_menu_action)


        open_file_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'blue-folder-open-document.png')),"Open file...",self)
         # open file method

        
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        self.file_menu.addAction(open_file_action)
        self.toolBar.addAction(open_file_action)

        save_file_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'disk.png')), "Save", self)
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        self.file_menu.addAction(save_file_action)
        self.toolBar.addAction(save_file_action)

        saveas_file_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'disk--pencil.png')), "Save As...", self)
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        self.file_menu.addAction(saveas_file_action)
        self.toolBar.addAction(saveas_file_action)

        self.print_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'printer.png')), "Print...", self)
        self.print_action.setStatusTip("Print current page")
        self.print_action.triggered.connect(self.file_print)
        self.file_menu.addAction(self.print_action)
        self.toolBar.addAction(self.print_action)


        """ Start and Stop recording audio """
        self.registrare_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'recoding.png')), "Record...", self)
        self.registrare_action.setStatusTip("Record the screen")
        self.registrare_action.triggered.connect(self.startRecording)
        self.file_menu.addAction(self.registrare_action)
        self.toolBar.addAction(self.registrare_action)


        self.registrare_actionStop = QAction(QIcon(os.path.join(pathFolder + 'images', 'StopRecordingAudio.png')), "Stop Record...", self)
        self.registrare_actionStop.setStatusTip("Stop recording Audio")
        self.registrare_actionStop.triggered.connect(self.stopRecording)
        self.file_menu.addAction(self.registrare_actionStop)
        self.toolBar.addAction(self.registrare_actionStop)


        self.video_import = QAction(QIcon(os.path.join(pathFolder + 'images', 'importVideo.png')), "Import video...", self)
        self.video_import.setStatusTip("Import Video")
        self.video_import.triggered.connect(self.videoImport)
        self.toolBar.addAction(self.video_import)

        ''' style for the text '''
        self.style_toolbar = QToolBar("Style")
        self.style_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.style_toolbar)
        
        self.boldAction = QtWidgets.QAction(QtGui.QIcon("images/bold.png"),"Bold",self)
        self.boldAction.triggered.connect(self.bold)
        self.style_toolbar.addAction(self.boldAction)

        self.edit_toolbar = QToolBar("Edit")
        self.edit_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.edit_toolbar)
        self.edit_menu = self.menuBar().addMenu("&Edit")

        self.undo_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'arrow-curve-180-left.png')), "Undo", self)
        self.undo_action.setStatusTip("Undo last change")
        self.undo_action.triggered.connect(self.editor.undo)
        self.edit_menu.addAction(self.undo_action)

        self.redo_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'arrow-curve.png')), "Redo", self)
        self.redo_action.setStatusTip("Redo last change")
        self.redo_action.triggered.connect(self.editor.redo)
        self.edit_toolbar.addAction(self.redo_action)
        self.edit_menu.addAction(self.redo_action)

        self.edit_menu.addSeparator()
        
        self.cut_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'scissors.png')), "Cut", self)
        self.cut_action.setStatusTip("Cut selected text")
        self.cut_action.triggered.connect(self.cutFunction)
        self.edit_toolbar.addAction(self.cut_action)
        self.edit_menu.addAction(self.cut_action)

        copy_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'document-copy.png')), "Copy", self)
        copy_action.setStatusTip("Copy selected text")
        #copy_action.triggered.connect(self.editor.copy)
        self.edit_toolbar.addAction(copy_action)
        self.edit_menu.addAction(copy_action)

        paste_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'clipboard-paste-document-text.png')), "Paste", self)
        paste_action.setStatusTip("Paste from clipboard")
        #paste_action.triggered.connect(self.editor.paste)
        self.edit_toolbar.addAction(paste_action)
        self.edit_menu.addAction(paste_action)

        select_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'selection-input.png')), "Select all", self)
        select_action.setStatusTip("Select all text")
        #select_action.triggered.connect(self.editor.selectAll)
        self.edit_menu.addAction(select_action)

        self.edit_menu.addSeparator()

        wrap_action = QAction(QIcon(os.path.join(pathFolder + 'images', 'arrow-continue.png')), "Wrap text to window", self)
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        self.edit_menu.addAction(wrap_action)


        self.Audio_toolbar = QToolBar("Edit")
        self.Audio_toolbar.setIconSize(QSize(20, 20))
        self.addToolBar(self.Audio_toolbar)

        self.Audio_option_menu = self.menuBar().addMenu("&Audio Option")
        
        # definizione del qthread per il riascolto dell'audio
        self.threadpool = QThreadPool()

        self.riascoltoAudio = QAction(QIcon(os.path.join(pathFolder + 'images', 'manoIcon.png')), "Listen current audio", self)
        self.riascoltoAudio.setStatusTip("Undo last change")
        self.riascoltoAudio.triggered.connect(self.riascolto_Audio)
        self.Audio_option_menu.addAction(self.riascoltoAudio)
        self.Audio_toolbar.addAction(self.riascoltoAudio)


        self.deleteAudio_Button = QAction(QIcon(os.path.join(pathFolder + 'images', 'deleteAudio.png')), "Delete Audio and Text", self)
        self.deleteAudio_Button.setStatusTip("Delete copybook")
        self.deleteAudio_Button.triggered.connect(self.deleteAudio_Function)
        self.Audio_option_menu.addAction(self.deleteAudio_Button)
        self.Audio_toolbar.addAction(self.deleteAudio_Button)

        self.deleteCopyBook = QAction(QIcon(os.path.join(pathFolder + 'images', 'deleteCopyBook.png')), "Delete Audio and Text", self)
        self.deleteCopyBook.setStatusTip("Delete copybook")
        self.deleteCopyBook.triggered.connect(self.deleteCopyBookFunction)
        self.Audio_option_menu.addAction(self.deleteCopyBook)
        self.Audio_toolbar.addAction(self.deleteCopyBook)

        self.NewAudio = QAction(QIcon(os.path.join(pathFolder + 'images', 'newFile.png')), "Create new 'copybook'", self)
        self.NewAudio.triggered.connect(self.newCopyBook)
        self.Audio_option_menu.addAction(self.NewAudio)
        self.Audio_toolbar.addAction(self.NewAudio)

        """ Botton to convert audio into text """
        self.convertAudio = QAction(QIcon(os.path.join(pathFolder + 'images', 'text-speech.png')), "Convert the audio of the copybook into text", self)
        self.convertAudio.triggered.connect(self.convertAudioToText)
        self.Audio_option_menu.addAction(self.convertAudio)
        self.Audio_toolbar.addAction(self.convertAudio)


        # Toglie l'opzione di cliccare il pulsante in quanto non viene caricato di default nessun file
        self.deleteCopyBook.setDisabled(True)
        self.convertAudio.setDisabled(True)
        self.NewAudio.setDisabled(True)
        self.riascoltoAudio.setDisabled(True)
        self.deleteAudio_Button.setDisabled(True)

        
        self.listwidget.doubleClicked.connect(self.on_clickMenuList)
        self.Audio_option_menu.addSeparator()
        


        
    def deleteCopyBookFunction(self, currentItem = None):
        if currentItem is None:
            currentItemTemp = currentItem
        else:
            currentItemTemp = self.currentTitle
            
        
        posizione = self.indice['file']['titolo'].index(currentItemTemp)

        ## Rimozione del file nameFile dalla cartella self.temp_
        os.remove(self.path + "/" + self.temp_ + "/" + self.indice['file']['file_testo'][posizione] + ".json")
        
        del self.indice['file']['titolo'][posizione]
        del self.indice['file']['audio'][posizione]
        del self.indice['file']['compressione'][posizione] 
        del self.indice['file']['video'][posizione]
        del self.indice['file']['file_testo'][posizione]
        self.indice['video_checksum'] -= 1 

        self.currentTitle = None
        self.currentTitleJSON = None

        self.editor.setDisabled(True)
        self.deleteAudio_Button.setDisabled(True)
        self.convertAudio.setDisabled(True)
        self.deleteCopyBook.setDisabled(True)
        self.riascoltoAudio.setDisabled(True)

        self.updateList_()

        print(self.indice)


    def bold(self):
        if self.editor.fontWeight() == QtGui.QFont.Bold:

            self.editor.setFontWeight(QtGui.QFont.Normal)

        else:
            self.editor.setFontWeight(QtGui.QFont.Bold)

        print(self.editor.toPlainText())
    

def launch():
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