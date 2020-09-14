import os
import sys
import json

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

if __name__ == '__main__':
    # To test 
    p = System()
    print(sys.platform)