from fastapi import WebSocket
from app.model.notification import NotificationOut

class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(
        self,
        user_id:str,
        websocket:WebSocket
    ):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id:str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_notification(
        self,
        user_id:str,
        notification:NotificationOut
    ):
        websocket = self.active_connections.get(user_id)

        if websocket:
            try:
                await websocket.send_json(notification.model_dump(mode="json"))
            except Exception as e:
                print(e)
                self.disconnect(user_id)

manager = ConnectionManager()