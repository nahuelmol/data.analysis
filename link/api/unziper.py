import base64
import zipfile
from io import BytesIO
import filetype

#from link.api.errs import WrongFileType

def unzip(file_str):
    bytes_file = base64.b64decode(file_str)
    file_like = BytesIO(bytes_file)
    kind = filetype.guess(bytes_file)
    if kind:
        if kind.extension != 'zip':
            return False, 'incorrect file type'
    else:
        return False, 'not a format'
    with zipfile.ZipFile(file_like, 'r') as zip_ref: #bytes_file must be a file-like object
        content_list = zip_ref.namelist()
        with zip_ref.open(content_list[0]) as f:
            file_data = f.read()
            base64_data = base64.b64encode(file_data).decode('utf-8')
            file = base64_data
            #I must return the file 
            return True, file

