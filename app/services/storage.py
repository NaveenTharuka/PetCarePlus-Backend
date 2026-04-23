from fastapi import UploadFile
import httpx
import os
from uuid import uuid4

BUCKET = "PetCarePlusReports"

async def upload_file(file: UploadFile, name : str):

    file_name_prefix = uuid4()
    file_ext = file.filename.split(".")[-1] if file.filename and "." in file.filename else "bin"
    
    safe_name = name.replace(" ", "_").replace("/", "_").replace("\\", "_")
    file_name = f"{safe_name}-{file_name_prefix}.{file_ext}"

    url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/{BUCKET}/{file_name}"

    headers = {
        "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}",
        "Content-Type": file.content_type or 'application/octet-stream'
    }

    content = await file.read()

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            url,
            headers=headers,
            content=content
        )

    if response.status_code not in [200, 201]:
        raise Exception(f"Upload failed: {response.text}")

    return file_name