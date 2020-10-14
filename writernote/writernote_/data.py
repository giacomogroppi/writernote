import json

def checkInserimento(stringa: str) -> bool:
    ''' controlla che ogni stringa sia contenuta in quella successiva '''
    i = 0
    lunghezza = len(stringa) - 1
    while i < lunghezza:
        if not stringa[i] in stringa[i + 1]:
            return False
        
        i += 1
        
        
        
        """ da eliminare
        k = 0
        while k < len(stringa[i-1]) and k < len(stringa[i]):
            if stringa[i-1] in stringa[i]:
                ''' vuol dire che è contenuta '''
                break

            if stringa[i][k] != stringa[i-1][k]:
                return False

            k += 1
        i += 1"""

    return True

def check1(text) -> bool:
    i = 1
    lunghezza = len(text)
    while i < lunghezza:
        if len(text[i]) <= len(text[i-1]) or text[i][-1] == ' ':
            ''' false se la lunghezza è diversa o se c'è uno spazio '''
            return False

        i += 1

    return True

def eliminazioneNFrasi(text: dict) -> dict:
    ''' 
    funzione che permette di eliminare più grasi registrate 
    nello stesso secondo, in modo da occupare meno spazio
    nel file finale *.writer 

    viene considerato il fatto che le strighe siano state
    tutte corrette, in quanto gli altri step sono già stati eseguiti 
    precedentemente
    '''
    if len(text['posizione_iniz']) != len(text['testinohtml']): return text

    i = 1
    lunghezza = len(text['posizione_iniz'])
    while i < lunghezza:
        if text['posizione_iniz'][i] == text['posizione_iniz'][i - 1]:
            ''' in questo modo se non ci sono più stringe '''
            del text['posizione_iniz'][i-1], text['testinohtml'][i - 1]
            
            ''' perchè la lunchezz è diminuita di uno '''
            lunghezza -= 1

        else:
            ''' in caso entrasse nel primo if bisogna rifare il controllo
            -> quindi non aumenta '''
            i += 1

    return text


def spacchettamento(text) -> dict:
    ''' funzione richiamata internamente che 
    aggiunge le stringe tra di loro '''

    ''' parte della funzione che aggiusta gli inserimenti di testo all'interno di una frase [e non alla fine] '''
    while not checkInserimento(text['testinohtml']):
        i = 1
        lunghezza = len(text['testinohtml'])
        while i < lunghezza:
            k = 0
            while k < len(text['testinohtml'][i-1]) and k < len(text['testinohtml'][i]):
                if text['testinohtml'][i][k] != text['testinohtml'][i-1][k] and k != len(text['testinohtml'][i-1]):
                    text['testinohtml'][i-1] = text['testinohtml'][i-1][:k] + text['testinohtml'][i][k] + text['testinohtml'][i-1][k:]
                    break

                k += 1

            i += 1

    ''' parte di funzione che aggiusta in caso di modifica al termina della stringa '''
    while True:
        if check1(text['testinohtml']):
            break

        i = 1

        lunghezza = len(text['testinohtml'])
        while i < lunghezza:
            if len(text['testinohtml'][i]) < len(text['testinohtml'][i-1]):
                difference = len(text['testinohtml'][i]) - len(text['testinohtml'][i-1])
                text['testinohtml'][i-1] = text['testinohtml'][i-1][:difference]

            if len(text['testinohtml'][i]) == len(text['testinohtml'][i-1]) or text['testinohtml'][i][-1] == ' ':
                del text['testinohtml'][i], text['posizione_iniz'][i]
                
                lunghezza -= 1
                
            else:
                ''' in caso entri nel primo if non deve aumentare il contatore in quanto deve rifare il controllo '''
                i += 1

    return text


def spacchetta(text: dict) -> dict:
    if not isinstance(text, dict):
        text = json.load(text)

    text = spacchettamento(text)

    text = eliminazioneNFrasi(text)

    return text



if __name__ == '__main__':
    ''' for the testing part '''
    
    with open("/home/giacomo/Scrivania/test.json") as fileC:
        fileC = json.load(fileC)
    
    with open("/home/giacomo/Scrivania/temp", 'w') as fileciao:
        fileciao.writelines("prima\n")
        for x in fileC['testinohtml']:
            fileciao.writelines("\n" + x)
    
    stringa = spacchetta(fileC)

    with open("/home/giacomo/Scrivania/temp", 'a') as fileciao:
        
        fileciao.writelines("\n\ndopo\n")
        for x in stringa['testinohtml']:
            fileciao.writelines('\n' + x)