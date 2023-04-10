import os
import zipfile
from io import BytesIO

from magic import from_buffer

from cloud_storage.config import get_settings

settings = get_settings()


def check_file_type(file_path: str):
    if os.path.isfile(file_path):
        return True
    elif os.path.isdir(file_path):
        return False
    raise FileNotFoundError


def create_directory(dir_path: str, dir_name: str):
    try:
        os.mkdir(f"{dir_path}{dir_name}")
    except OSError:
        return False
    else:
        return True


def delete_file(file_path: str, file_name: str):
    path_file = f"{file_path}{file_name}"
    type_file = check_file_type(path_file)
    try:
        if type_file:
            os.remove(path_file)
        elif not type_file:
            os.rmdir(path_file)
    except OSError:
        return False
    else:
        return True


def files_in_directory(path: str):
    return os.listdir(path)


def zip_files(path: str, dir_name: str):
    file_list = files_in_directory(path)
    io = BytesIO()
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zipped:
        for fpath in file_list:
            zipped.write(filename=f"{path}/{fpath}", arcname=f"{dir_name}/{fpath}")
        zipped.close()
    return iter([io.getvalue()])


def get_file_size(path_file: str):
    return os.path.getsize(path_file)


def get_mime_type(head_file: bytes):
    file_mime_type = from_buffer(head_file, mime=True)
    return file_mime_type

# def delete_file(file_path: str):
