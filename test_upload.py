import asyncio
import httpx
from app.database import DB_URL
import os

async def test():
    BUCKET = 'PetCarePlus'
    file_name = 'test-1234.txt'
    # Use correct URL
    url = f"https://xkoekzhihxqwrsvxvyiz.supabase.co/storage/v1/object/{BUCKET}/MedicalReports/{file_name}"
    headers = {
        'Authorization': f"Bearer {os.getenv('SUPABASE_SERVICE_KEY')}",
        'Content-Type': 'text/plain'
    }
    content = b'test content'
    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, content=content)
        print("Status code:", response.status_code)
        print("Response:", response.text)

asyncio.run(test())
