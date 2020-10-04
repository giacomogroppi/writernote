import os
import zipfile
import tempfile
import json

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
    try:
        import shutil
        shutil.make_archive(path + "/" + nameFile, 'zip', "/tmp/writernote/" + temp_)

        base = os.path.splitext(path + "/" + nameFile)[0]

        os.rename(path + "/" + nameFile + ".zip", base + ".writer")

        return True
    except PermissionError:
        return False

if __name__ == '__main__':
    """ Test for modify the zip file """
    testo = 'This data did not exist in a file before being added to the ZIP file'
    namefile_zip = 'ciao.zip'
    namefile_to_compress = 'test.txt'
    
    #updateZip(namefile_zip, namefile_to_compress, testo)
    