import json

def checkInserimento(stringa: str) -> bool:
    ''' controlla che ogni stringa sia contenuta in quella successiva '''
    i = 0
    lunghezza = len(stringa) - 1
    #print("checkInserimento start")
    while i < lunghezza:
        lencompare = len(stringa[i+1]) - len(stringa[i])
        #if lencompare > 0 and stringa[i][:lencompare] == stringa[i][:lencompare]: 
        #    pass

        if lencompare <= 0 and stringa[i][:-abs(lencompare)] == stringa[i+1]:
            ''' se entra vuol dire che 
                come prima cosa la stringa[i] è più lunga di abs(lencompare)
                rispetto a stringa[i+1]

                e come seconda cosa è stato eliminato del testo alla fine
                in caso non fosse stato eliminato del testo alla fine
                non entra e nel prossimo elif farà il return false
             '''
            pass

        

        elif not stringa[i] in stringa[i + 1]:
            #print("checkInserimento stop")
            #print("\n",stringa[i],"\n", stringa[i+1])
            #print(len(stringa[i]), len(stringa[i+1]))
            return False
        
        i += 1
        

    return True

def check1(text) -> bool:
    print("check1 start")
    i = 1
    lunghezza = len(text)
    while i < lunghezza:
        if len(text[i]) <= len(text[i-1]) or text[i][-1] == ' ':
            ''' false se la lunghezza è diversa o se c'è uno spazio '''
            print("check1 stop")
            return False

        i += 1
    print("check1 stop")
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
    print("primowhile start")
    i = 1
    lunghezzaLista = len(text['testinohtml'])
    while i < lunghezzaLista:
        while not checkInserimento(text['testinohtml'][:i]):
            ''' in questo modo sistema tutte le stringhe fino a quella considerata in quel momento '''
            for j in range(1, i+1):
                if len(text['testinohtml'][j]) > len(text['testinohtml'][j - 1]):###FUNZIONA
                    ''' deve sistemare la stringa se e solo se quella dopo, all'interno della lista è più lunga, altrimenti vuol dire che è  '''
                    k = 0
                    while k < len(text['testinohtml'][j-1]) and k < len(text['testinohtml'][j]):
                        if text['testinohtml'][j][k] != text['testinohtml'][j-1][k] and k != len(text['testinohtml'][j-1]):
                            #print("\nIN TO CULO")
                            #print("STRINGA-1:     ", text['testinohtml'][j-1], "\nSTRINGADUE:     "+text['testinohtml'][j])
                            text['testinohtml'][j-1] = text['testinohtml'][j-1][:k] + text['testinohtml'][j][k] + text['testinohtml'][j-1][k:]
                                
                            #print("STRINGA-1 DOPO:", text['testinohtml'][j-1], "\nSTRINGADUEDOPO: "+text['testinohtml'][j])
                            
                            break

                        k += 1
                
                elif len(text['testinohtml'][j]) <= len(text['testinohtml'][j - 1]):
                    ''' parte della funzione funzione che gestisce di correggere l'eliminazione di testo in mezzo '''
                    k = 0
                    while k < len(text['testinohtml'][j-1]) and k < len(text['testinohtml'][j]):
                        #print("entra nel ciclo")
                        if text['testinohtml'][j][k] != text['testinohtml'][j-1][k]:
                            #print("\nSTOCAZZO")
                            #print("STRINGA-1:     ", text['testinohtml'][j-1], "\nSTRINGADUE:     "+text['testinohtml'][j])
                            #print(j)                            
                            #print(text['testinohtml'][j-1][:k])
                            #print(text['testinohtml'][j][:k])
                        
                            text['testinohtml'][j-1] = text['testinohtml'][j-1][:k] + text['testinohtml'][j-1][k+1:]
                            
                            #print("STRINGA-1 DOPO:", text['testinohtml'][j-1], "\nSTRINGADUEDOPO: "+text['testinohtml'][j])

                            break
                        
                        k += 1

        ''' aumenta il range della lista per il controllo '''
        i += 1
    
    #print("primowhile stop")

    #print("secondowhile start")
    ''' parte di funzione che aggiusta in caso di modifica al termina della stringa '''
    while not check1(text['testinohtml']):
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

    print("secondowhile stop")
    return text


def spacchetta(text: dict) -> dict:
    if not isinstance(text, dict):
        text = json.load(text)

    text = spacchettamento(text)
    #print("eliminazioneNFrasi start")
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
            fileciao.writelines('\n\n\n\n' + x)