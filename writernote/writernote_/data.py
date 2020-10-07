import json
import sys
import os

def check(text) -> bool:
    i = 0
    while True:
        if (i+1) == len(text):
            break
        
        if i == 0: 
            pass
        elif len(text[i]) <= len(text[i-1]) or text[i][-1] == ' ':
            ''' false se c'è un elemento che non va bene  '''
            return False
        
        i += 1 

    return True

def spacchettamento(text) -> dict:
    ''' funzione che aggiorna il testo '''

    while True:
        if check(text['testinohtml']):
            break

        i = 0
        
        while True:
            if (i+1) == len(text['testinohtml']):
                break
            
            if i == 0: 
                pass
                
            elif len(text['testinohtml'][i]) < len(text['testinohtml'][i-1]):
                difference = len(text['testinohtml'][i]) - len(text['testinohtml'][i-1])
                print("\ndifferenza: {}, contatore: {}".format(difference, i))
                text['testinohtml'][i-1] = text['testinohtml'][i-1][:difference]
            
            if len(text['testinohtml'][i]) == len(text['testinohtml'][i-1]) or text['testinohtml'][i][-1] == ' ':
                print("lunghezza: {}, indice {}".format(len(text['testinohtml']), i))
                del text['testinohtml'][i], text['posizione_iniz'][i]
                i -= 1
                print("lunghezza: {}, indice {}".format(len(text), i))
            
            i += 1 

    return text

if __name__ == '__main__':
    testoTemp = '/home/giacomo/Scrivania/test.json'
    with open(testoTemp) as file:
        testoTemp = json.load(file)

    ciao = spacchettamento(testoTemp)
    with open("/home/giacomo/Scrivania/temp", 'w') as file:
        for x in ciao:
            file.writelines("\n" + x)
        