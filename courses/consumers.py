# courses/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if self.user.is_authenticated:
            self.group_name = f"user_progress_{self.user.id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, close_code):
        if self.user.is_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        """
        Handles data received from the WebSocket client.
        Example input:
        {
            "lesson_id": 5,
            "status": "completed"
        }
        """
        data = json.loads(text_data)
        lesson_id = data.get("lesson_id")
        status = data.get("status")

        # This is where you would update user progress in DB (optional)
        # await self.update_user_progress(lesson_id)

        # Send real-time feedback to this user
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "progress.update",
                "message": f"Lesson {lesson_id} marked as {status}!"
            }
        )

    async def progress_update(self, event):
        await self.send(text_data=json.dumps({
            "message": event["message"]
        }))

    @database_sync_to_async
    def update_user_progress(self, lesson_id):
        # You can implement real DB update logic here if needed
        # For example: mark lesson_id as completed for self.user
        pass
