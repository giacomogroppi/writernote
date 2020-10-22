#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from setuptools import setup

def findImages() -> list:
    from os import walk

    name = []
    for (dirpath, dirnames, filenames) in walk('writernote/images'):
        #print(filenames)

        for x in filenames:
            name.append("writernote/images/" + x)
    
    finale = ['writernote/indice.json',
            #'writernote/permission.json',
            'writernote/default_file.json',
            'writernote/config.json',
            'writernote/images/importVideo.png']
    finale.extend(name)

    return finale

setup(
    name = "writernote",
    version = "1.0",
    author = "Giacomo Groppi",
    author_email = "giamg01@gmail.com",
    #install_requires = [
    #    'pyqt5'
    #],
    packages = ["writernote_"],
    description = "Demo of packaging a Python script",
    license = "",
    #url = "https://github.com/giacomogroppi/Writernote",
    #packages=find_packages(exclude=['ciao.writer']),
    scripts = ['writernote/writernote'],
    
    data_files = [
        ('images/', 
            findImages()
        )
    ],
    package_dir = {"": "writernote"},

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)'
    ],
    #install_requires=[
    #  'setuptools',
    #   'wheel',
    #   'pydub',
    #   'SpeechRecognition',
    #   'psutil',
    #   'googletrans',
    #   'nvpy',
    #   'Wave',
    #   'pytesseract'
    #]
)


