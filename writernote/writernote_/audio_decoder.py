from pydub.silence import split_on_silence
import speech_recognition as sr
import os
import psutil
import time
import socket
import re
import random as random
from os import path
from pydub import AudioSegment
from googletrans import Translator
from random import randrange
from datetime import datetime
import pytesseract
import io
import sys
from PyQt5 import QtWidgets


class Video():
    def __init__(self, path, temp_, nameAudio):
        self.temp_ = temp_
        self.path = path
        self.nameAudio = nameAudio
        

    def match_target_amplitude(self, aChunk, target_dBFS):
        ''' Normalize given audio chunk '''
        change_in_dBFS = target_dBFS - aChunk.dBFS
        return aChunk.apply_gain(change_in_dBFS)

    def delAudio(self, name):
        if sys.platform == "linux":
            os.system("rm -r " + name + "*") 

    def decoder(self):
        """
        funzione che traduce l'audio nel testo
        """

        language = 'it-IT'
        
        src = "/tmp/writernote/" + self.temp_ + "/" + self.nameAudio
        
        nomeTemp = str(datetime.now()).replace(" ", "").replace(":", "")
        c = 0
        while True:
            if not os.path.exists("/tmp/writernote/" + self.temp_ + "/" + nomeTemp + str(c)): break
            c += 1
        nomeTemp = "/tmp/writernote/" + self.temp_ + "/" + nomeTemp + str(c) + ".wav"

        """ Codifica il file in un formato in cui google non ha problemi a leggerlo """
        #print("ffmpeg -i " + src + " " + nomeTemp)
        os.system("ffmpeg -i " + src + " " + nomeTemp)
        
        testo_array = []

        audio_originale = AudioSegment.from_wav(nomeTemp)

        try:
            media_chunks_volume = audio_originale.dBFS
        except:
            media_chunks_volume = None


        if str(media_chunks_volume) != '-inf' and media_chunks_volume is not None:
            
            print("media_chunks_volume: ",media_chunks_volume)
            chunks = split_on_silence (
                audio_originale,
                min_silence_len = 250,
                
                silence_thresh = float(media_chunks_volume + media_chunks_volume*0.3),
                keep_silence = 200
            )

            # Ogni volta che salva un file in temporaneo poi fa un .append(nome_chuck) per poterlo poi riprendere
            nomi_file = []

            for i, chunk in enumerate(chunks):
                silence_chunk = AudioSegment.silent(duration=500)
                
                audio_chunk = silence_chunk + chunk + silence_chunk
                
                normalized_chunk = self.match_target_amplitude(audio_chunk, -20.0)
                
                chunk_name = nomeTemp + "_" + str(i) + ".wav"
                normalized_chunk.export(
                    chunk_name,
                    bitrate = "192k",
                    format = "wav"
                )

                nomi_file.append(chunk_name)
        else:
            """
            A questo punto se il volume è troppo basso e non si riesce a capire bene la
            soglia del parlato, si può direttamente mandare tutto l'audio a google, senza
            neanche provare a tagliarlo
            """
            nomi_file = []
            nomi_file.append(nomeTemp)





        if testo_array is None:
            """
            Vuol dire che la funzione per tagliare i silenzi non è riuscita -->
            Appende a nomi_file direttamente il file compresso con ffmpeg
            """
            nomi_file.append(nomeTemp)


        try:
            #inizializzazione della classe come recognizer
            r = sr.Recognizer()


            def audio_direct(dst, language, verifica = True):
                """
                Fa la traduzione diretta a google e dopo manda il testo
                """
                try:
                    sound = dst
                    audio = sr.AudioFile(sound)
                    with audio as source:
                        audio_content = r.record(source)


                    testo_tradotto_intero = r.recognize_google(
                                                            audio_content,
                                                            language=language,
                                                            show_all=True
                                                            )

                    print(testo_tradotto_intero)

                    if not testo_tradotto_intero:
                        """ If it is [] --> return false and '' """
                        return False, ''

                    testo_tradotto_intero = testo_tradotto_intero['alternative'][0]['transcript']

                    return True, testo_tradotto_intero

                except:
                    return False, 0  

            try:
                for x in nomi_file:
                    """
                    Fa la traduzione in caso ci siano più di un chuck
                    E appende tutto a testo_array
                    """

                    sound = x

                    #Speech recognition
                    audio = sr.AudioFile(sound)
                    with audio as source:
                        audio_content = r.record(source)

                    testo_temporaneo = r.recognize_google(
                                                audio_content,
                                                language=language
                                            )

                    testo_array.append(testo_temporaneo)


            except:
                """
                In questo caso se ha riscontrato qualche errore nella traduzione
                lascia stare e invia solo quello completo
                """

                testo_array.clear()
                nomi_file.clear()

            testo = ''
            for i, x in enumerate(testo_array):
                testo = testo + str(x)
                if i < len(testo_array) - 1:
                    testo = testo + ", "
            


            if testo_array: # If the array is not empty the testo_array return True
                """ Se la traduzione con i silenzi ha funzionato """
                """ Fa la traduzione solamente senza direttamente i silenzi """
                self.delAudio(nomeTemp)
                return True, testo


            else:
                """ Se la traduzione con i silenzi ha fallito """
                
                if len(nomi_file) < 2:
                    
                    verifica, testo_funzione = audio_direct(nomeTemp, language, False)
                    if verifica:
                        self.delAudio(nomeTemp)
                        return True, testo_funzione
                    
                
                # bot.sendMessage(chat_id, str(testo_funzione), reply_to_message_id=msg['message_id'])
                

            if len(nomi_file) > 1:
                """ manda il messaggio in caso si siano divisi anche i silenzi """
                verifica, testo = audio_direct(nomeTemp, language)
                self.delAudio(nomeTemp)
                return True, 0

        except Exception as e:
            print(e)
            self.delAudio(nomeTemp)
            return False, 0

        return False, 0

    def scissione(self):

        self.audioPosition = self.path
        """
        Separa il video dall'audio
        """

        import datetime
        date = str(datetime.datetime.now())
        date = date.replace(" ", "").replace("-", "")
        print("date: ", date)
        i = 0
        while True:
            if not os.path.exists(self.temp_ + "/" + date + str(i) + ".mp3"):
                nome_Audio_temp = date + str(i) + ".mp3"
                break

            i += 1
                
        print(nome_Audio_temp)
        # self.path in questo caso è il nome del file video
        command_shell = "ffmpeg -i " + self.path + " -ab 600k -ac 2 -ar 44100 -vn /tmp/writernote/" + self.temp_ + "/" + nome_Audio_temp + " -threads nproc"

        os.system(command_shell)

            
        os.system("rm -r " + "log_" + nome_Audio_temp[:-4] + ".txt")
        
        return True, nome_Audio_temp

            
    

