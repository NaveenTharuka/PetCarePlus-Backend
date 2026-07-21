from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.websocket.manager import manager

router = APIRouter()

@router.websocket("/ws/notifications/{user_id}")
async def notification_socket(
    webSocket:WebSocket,
    user_id:str
):
    await manager.connect(
        user_id,
        webSocket
    )
    try:
        while True:
            await webSocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)