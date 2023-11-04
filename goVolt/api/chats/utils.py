from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()

@async_to_sync
async def send_message_consumer(message, channel_name):

    await channel_layer.send(channel_name, {
        'type': 'chat.message',
        'message': message
    })