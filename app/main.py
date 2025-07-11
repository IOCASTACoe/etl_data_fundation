
import os
import uuid
from typing import List

from fastapi import FastAPI, UploadFile, File
import os
from dotenv import dotenv_values, load_dotenv

import app.src.config as settings
from app.src.main_task import main

app = FastAPI()


@app.post("/uploadfiles/")
async def upload_files(files: List[UploadFile] = File(...)):
    
    main_path: str = str(uuid.uuid4())
    directory_path = f"{settings.TEMP_FILES}{main_path}"
    os.makedirs(directory_path, exist_ok=True) 
    for file in files:
        contents = await file.read()
        
        with open(f"{directory_path}/{file.filename}", "wb") as f:
            f.write(contents)

    main(main_path)
    return {"filenames": [file.filename for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    with open(f"{settings.TEMP_FILES}{file.filename}", "wb") as f:
        f.write(await file.read())
    return {"filename": file.filename}
