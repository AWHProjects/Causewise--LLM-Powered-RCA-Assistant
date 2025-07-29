import os
from werkzeug.utils import secure_filename

def save_uploaded_file(uploaded_file, folder='data'):
    filename = secure_filename(uploaded_file.filename)
    filepath = os.path.join(folder, filename)
    uploaded_file.save(filepath)
    return filepath