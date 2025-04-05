import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel
from uuid import uuid4
import shutil

app = FastAPI()

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory metadata storage
image_store: List[dict] = []

class ImageMeta(BaseModel):
    id: str
    filename: str
    title: str
    description: str
    tags: List[str]

@app.post("/upload/", response_model=ImageMeta)
async def upload_image(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: str = Form(...),
    tags: str = Form("")
):
    image_id = str(uuid4())
    filename = f"{image_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    metadata = {
        "id": image_id,
        "filename": filename,
        "title": title,
        "description": description,
        "tags": [tag.strip() for tag in tags.split(",") if tag.strip()]
    }
    image_store.append(metadata)
    return metadata

@app.get("/images/", response_model=List[ImageMeta])
def list_images():
    return image_store

@app.get("/images/{image_id}")
def view_image(image_id: str):
    image = next((img for img in image_store if img["id"] == image_id), None)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    file_path = os.path.join(UPLOAD_FOLDER, image["filename"])
    return FileResponse(file_path, media_type="image/*", filename=image["filename"])

@app.delete("/images/{image_id}", status_code=204)
def delete_image(image_id: str):
    global image_store
    image = next((img for img in image_store if img["id"] == image_id), None)
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")

    file_path = os.path.join(UPLOAD_FOLDER, image["filename"])
    if os.path.exists(file_path):
        os.remove(file_path)

    image_store = [img for img in image_store if img["id"] != image_id]
    return

if __name__ == "__main__":
    app.run()