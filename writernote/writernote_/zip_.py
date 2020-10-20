import os
import zipfile
import tempfile
import json

def extractAll(zipname, path, temporaneo, username):
    # Extract all file 
    import os
    if username is None:
        #linux
        pathExtract = path + "/" + zipname
    else:
        pathExtract = path + "\\" + zipname

    print(pathExtract)

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

def compressFolder(path: str, temp_: str, nameFile: str, username: str = None) -> bool:
    import shutil
    if username is None:
        ''' it means we are on linux  '''
        pathtemp = "/tmp/writernote"
        path1 = path + "/" + nameFile
        path1__ = pathtemp + "/" + temp_
        path2 = path + "/" + nameFile
        path3 = path + "/" + nameFile + ".zip"

    else:
        pathtemp = "C:\\Users\\" + username + "\\AppData\\Local\\Temp\\writernote"
        path1 = path + "\\" + nameFile
        path1__ = pathtemp + "\\" + temp_
        path2 = path + "\\" + nameFile
        path3 = path + "\\" + nameFile + ".zip"

    path1_ = 'zip' 
    path3_ = ".writer"

    try:
        if username is not None and os.path.exists(path1):
            os.remove(path1)
        
        shutil.make_archive(path1, path1_, path1__)
        base = os.path.splitext(path2)[0]

        os.rename(path3, base + path3_)

        return True
    except PermissionError:
        return False
    except:
        return False

if __name__ == '__main__':
    """ Test for modify the zip file """
    testo = 'This data did not exist in a file before being added to the ZIP file'
    namefile_zip = 'ciao.zip'
    namefile_to_compress = 'test.txt'
    
    #updateZip(namefile_zip, namefile_to_compress, testo)
    