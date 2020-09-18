import os
import zipfile
import tempfile
import json

#def updateZip(zipname, filename, data):
#    # generate a temp file
#    try:
#        tmpfd, tmpname = tempfile.mkstemp(dir=os.path.dirname(zipname))
#        os.close(tmpfd)
#
#        # create a temp copy of the archive without filename            
#        with zipfile.ZipFile(zipname, 'r') as zin:
#            with zipfile.ZipFile(tmpname, 'w') as zout:
#                zout.comment = zin.comment # preserve the comment
#                for item in zin.infolist():
#                    if item.filename != filename:
#                        zout.writestr(item, zin.read(item.filename))
#
#        # replace with the temp archive
#        os.remove(zipname)
#        os.rename(tmpname, zipname)
#
#        # now add filename with its new data
#        with zipfile.ZipFile(zipname, mode='a', compression=zipfile.ZIP_DEFLATED) as zf:
#            zf.writestr(filename, data)
#        return True
#
#    except Exception as e:
#        print(str(e))
#
#        return False 
#

#def readeZip(zipname, filename):
#    with zipfile.ZipFile(zipname, mode='r', compression=zipfile.ZIP_DEFLATED) as zf:
#        testo = zf.read(filename)
#
#    testo = json.loads(testo)
#    return testo


#def returnAudio(zipname, filename):
#    with zipfile.ZipFile(zipname, mode='r', compression=zipfile.ZIP_DEFLATED) as zf:
#        audio = zf.open(filename)
#
#    return audio

#def createEmpty(zipname):
#    empty_zip_data = 'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
#    if 1:
#        with zipfile.ZipFile(zipname, mode='w', compression=zipfile.ZIP_DEFLATED) as zf:
#            zf.write(empty_zip_data)
#        return True
#    try :
#        print("")
#    except Exception as e:
#        print(str(e))
#        return False

def extractAll(zipname, path, temporaneo):
    # Extract all file 
    import os
    try:
        with zipfile.ZipFile(path + "/" + zipname, mode='r') as zf:
            zf.extractall("/tmp/writernote/" + temporaneo)
        return True
        
    except PermissionError:
        raise PermissionError("We had a problem with the permission")

    except Exception as e:
        print(str(e))
        return False

def compressAll(path, temp_, nameFile):
    try:
        def zipdir(path, ziph):
            for root, dirs, files in os.walk(path):
                print(root, dirs, files)
                for file in files:
                    ziph.write(os.path.join(file))

        if os.path.splitext(nameFile)[1] != ".writer":
            zipf = zipfile.ZipFile(path + "/" + nameFile + ".writer", 'w', compression=zipfile.ZIP_DEFLATED)
        else:
            zipf = zipfile.ZipFile(path + "/" + nameFile, "w", compression=zipfile.ZIP_DEFLATED)

        zipdir(temp_ + "/", zipf)
        zipf.close()

        
        return True

    except Exception as e:
        print(str(e))
        return False

def compressFolder(path, temp_, nameFile):
    import shutil
    shutil.make_archive(path + "/" + nameFile, 'zip', "/tmp/writernote/" + temp_)
    
    base = os.path.splitext(path + "/" + nameFile)[0]
    os.rename(path + "/" + nameFile + ".zip", base + ".writer")

    return True

if __name__ == '__main__':
    """ Test for modify the zip file """
    testo = 'This data did not exist in a file before being added to the ZIP file'
    namefile_zip = 'ciao.zip'
    namefile_to_compress = 'test.txt'
    
    #updateZip(namefile_zip, namefile_to_compress, testo)
    