import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
import shutil
from models import ImageMeta
from s3handler import upload_image_to_s3, delete_file_from_s3
from dynamohandler import save_image_metadata_to_dynamodb, list_all_items, delete_metadata_from_dynamodb, get_image_by_id, search_images

app = FastAPI()

UPLOAD_FOLDER = "uploads"

# In-memory metadata storage
image_store: List[dict] = []

@app.post("/upload/", response_model=ImageMeta)
async def upload_image(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form("")
):
    image_id = str(uuid4())
    filename = f"{image_id}_{file.filename}"
    # file_path = os.path.join(UPLOAD_FOLDER, filename)

    upload_image_to_s3(file.file,UPLOAD_FOLDER,filename)

    metadata = {
        "id": image_id,
        "filename": filename,
        "title": title,
        "description": description,
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()]
    }
    image_store.append(metadata)
    save_image_metadata_to_dynamodb(metadata)
    return metadata

@app.get("/images/", response_model=List[ImageMeta])
def list_images():
    data = list_all_items()
    return data

@app.get("/images/{image_id}")
def view_image(image_id: str):
    image = get_image_by_id(image_id)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@app.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: str):
    image = get_image_by_id(image_id)
    delete_file_from_s3(UPLOAD_FOLDER, image["filename"] )
    delete_metadata_from_dynamodb(image_id)
    return image

@app.get("/search")
def search_images_endpoint(
    filename: Optional[str]=None,
    title: Optional[str]=None,
    description: Optional[str]=None,
    tag: Optional[str]=None
):
    return search_images(filename=filename, title=title, description=description, tag=tag)
