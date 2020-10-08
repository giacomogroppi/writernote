import json
import check

def spacchetta(text) -> dict:
    if not isinstance(text, dict):
        text = json.load(text)

    text = check.spacchettamento(text)

    return text

if __name__ == '__main__':
    ''' for the testing part '''
    
    with open("/home/giacomo/Scrivania/test.json") as fileC:
        fileC = json.load(fileC)
    
    with open("/home/giacomo/Scrivania/temp", 'w') as fileciao:
        fileciao.writelines("prima\n")
        for x in fileC['testinohtml']:
            fileciao.writelines("\n" + x)
    
    stringa = check.spacchettamento(fileC)

    with open("/home/giacomo/Scrivania/temp", 'a') as fileciao:
        
        fileciao.writelines("\n\ndopo\n")
        for x in stringa['testinohtml']:
            fileciao.writelines('\n' + x)