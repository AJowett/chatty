from . import api 
from ..models import Channel, User, Message
from flask_login import login_required

@api.route('/api/channels')
@login_required
def channel_list():
    channel_list = Channel.query.order_by(Channel.name).all()
    return {'channels': [{'name': channel.name, 'id': channel.id} for channel in channel_list]}

@api.route('/api/channel/<channel_id>/messages')
@login_required
def channel_past_messages(channel_id):
    messages = Message.query.filter_by(channel_id=channel_id).order_by(Message.timestamp).all()
    data = {'type': 'message_list',
            'messages': []}
    for message in messages:
        author = User.query.filter_by(id=message.user_id).first()
        message_dict = {"type": "message_channel", 
                        "id": str(message.id),
                        "channel_id": message.channel_id, 
                        "username": author.username, 
                        "timestamp": str(message.timestamp),
                        "profile": author.gravatar(),
                        "body": message.body}
        data['messages'].append(message_dict)
    return data
