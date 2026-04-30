from fastapi import UploadFile, HTTPException
import httpx
import os

BUCKET = "PetCarePlus"

async def upload_file(file: UploadFile, file_name : str, folder : str):

    url = f"{os.getenv('SUPABASE_URL')}/storage/v1/object/{BUCKET}/{folder}/{file_name}"

    headers = {
        "Authorization": f"Bearer {os.getenv('SUPABASE_KEY')}",
        "Content-Type": file.content_type or 'application/octet-stream'
    }

    content = await file.read()

    file_path = f"{folder}/{file_name}"

    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                url,
                headers=headers,
                content=content
            )
        
        if response.status_code not in [200, 201]:
            raise HTTPException(status_code=400, detail="Bad request")

        return file_path

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    