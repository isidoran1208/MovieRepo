from channels.generic.websocket import AsyncWebsocketConsumer


class MovieConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("Movie", self.channel_name)
        await self.accept()

    async def new_Movie(self, event):
        await self.send(event['data'])

class CommentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("Comment", self.channel_name)
        await self.accept()

    async def new_Comment(self, event):
        await self.send(event['data'])

class ReactionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("Reaction", self.channel_name)
        await self.accept()

    async def new_Reaction(self, event):
        await self.send(event['data'])