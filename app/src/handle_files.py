
import glob
import logging
import os
import pathlib

import app.src.config as settings

logger = logging.getLogger(__name__)

def get_path(midle_path: str) -> str:
    return pathlib.Path(settings.TEMP_FILES, midle_path).__str__()

def find_files_with_extension_glob(directory, extension) -> list[str]:
    pattern = os.path.join(directory, f"*{extension}")
    return glob.glob(pattern)

def valid_files(dir_path: str, extension: str) -> pathlib.Path:
    file_path = pathlib.Path("")
    for ext in settings.VALID_FILES:
        result = find_files_with_extension_glob(directory=dir_path, extension=extension)
        if len(result) > 1:
            raise Exception(
                f"Existem {len(result)} arquivos no diretório {dir_path} com a extensão {extension}."
            )
        elif len(result) == 0:
            raise Exception(
                f"Não existe arquivos no diretório {dir_path} com a extensão {extension}."
            )
        file_path = pathlib.Path(result[0])

    return file_path