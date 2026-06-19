from fastapi import UploadFile, HTTPException
from app.supabase import supabase
import httpx
import os

BUCKET = "PetCarePlus"

async def upload_file(file: UploadFile, file_name: str, folder: str):

    try:
        content = await file.read()

        file_path = f"{folder}/{file_name}"

        response = supabase.storage.from_(BUCKET).upload(
            path=file_path,
            file=content,
            file_options={
                "content-type": file.content_type or "application/octet-stream",
                "upsert": "true"
            }
        )

        # Supabase returns error info differently depending on version
        if hasattr(response, "error") and response.error:
            raise HTTPException(status_code=400, detail=response.error.message)

        return f"{file_path}"

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    