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



def spacchettamento(text) -> dict:
    ''' funzione che aggiorna il testo '''


    while not check(text['testinohtml']):
        i = 1
        while i < len(text['testinohtml']):
            k = 0
            while k < len(text['testinohtml'][i-1]) and k < len(text['testinohtml'][i]):
                #if len(text['testinohtml'][i]) < len(text['testinohtml'][i-1]):
                #    print("break1")
                #    break

                if text['testinohtml'][i][k] != text['testinohtml'][i-1][k] and k != len(text['testinohtml'][i-1]):
                    text['testinohtml'][i-1] = text['testinohtml'][i-1][:k] + text['testinohtml'][i][k] + text['testinohtml'][i-1][k:]
                    break

                k += 1

            i += 1

    while True:
        if check1(text['testinohtml']):
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
