import json

def check(stringa)-> bool:
    i = 1
    while i < len(stringa):
        k = 0
        while k < len(stringa[i-1]) and k < len(stringa[i]):
            if stringa[i-1] in stringa[i]:
                ''' vuol dire che è contenuta '''
                break

            if stringa[i][k] != stringa[i-1][k]:
                return False

            k += 1
        i += 1


    return True

def check1(text) -> bool:
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
    while True:
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
    ''' funzione che aggiorna il testo '''


    while not check(text['testinohtml']):
        i = 1
        while i < len(text['testinohtml']):
            k = 0
            while k < len(text['testinohtml'][i-1]) and k < len(text['testinohtml'][i]):
                if text['testinohtml'][i][k] != text['testinohtml'][i-1][k] and k != len(text['testinohtml'][i-1]):
                    text['testinohtml'][i-1] = text['testinohtml'][i-1][:k] + text['testinohtml'][i][k] + text['testinohtml'][i-1][k:]
                    break

                k += 1

            i += 1

    while True:
        if check1(text['testinohtml']):
            break

        i = 1

        while True:
            if (i+1) == len(text['testinohtml']):
                break


            elif len(text['testinohtml'][i]) < len(text['testinohtml'][i-1]):
                difference = len(text['testinohtml'][i]) - len(text['testinohtml'][i-1])
                text['testinohtml'][i-1] = text['testinohtml'][i-1][:difference]

            if len(text['testinohtml'][i]) == len(text['testinohtml'][i-1]) or text['testinohtml'][i][-1] == ' ':
                #print("lunghezza: {}, indice {}".format(len(text['testinohtml']), i))
                del text['testinohtml'][i], text['posizione_iniz'][i]
                i -= 1
                #print("lunghezza: {}, indice {}".format(len(text), i))

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