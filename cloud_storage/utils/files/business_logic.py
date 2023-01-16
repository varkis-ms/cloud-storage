import os
import zipfile
from io import BytesIO

from magic import from_buffer

from cloud_storage.config import get_settings

settings = get_settings()


def create_directory(dir_name: str, path: str = settings.STORAGE_PATH):
    try:
        os.mkdir(f"{path}/{dir_name}")
    except OSError:
        return f"Failed to create '{dir_name}' directory"
    else:
        return f"'{dir_name}' directory successfully created"


def delete_directory(dir_name: str, path: str = settings.STORAGE_PATH):
    try:
        os.rmdir(f"{path}/{dir_name}")
    except OSError:
        return f"Failed to delete '{dir_name}' directory"
    else:
        return f"'{dir_name}' directory successfully deleted"


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


def get_file_size(file_path: str):
    file_path = f"{settings.STORAGE_PATH}{file_path}"
    return os.path.getsize(file_path)


def get_mime_type(head_file: bytes):
    file_mime_type = from_buffer(head_file, mime=True)
    return file_mime_type
