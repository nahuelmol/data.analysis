import base64
import zipfile
from io import BytesIO
import filetype

def unzip(file_str):
    file_byte = base64.b64decode(file_str)
    file_like = BytesIO(file_byte)
    kind = filetype.guess(bytes_byte)
    if kind:
        if kind.extension != 'zip':
            return False, 'ERR: incorrect file type'
    else:
        return False, 'ERR: is not possible to read the extension'

    with zipfile.ZipFile(file_like, 'r') as zip_ref: #file_byte must be a file-like object
        content_list = zip_ref.namelist()
        with zip_ref.open(content_list[0]) as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
            #I must return the file 
            return True, file

