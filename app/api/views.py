from . import api 
from ..models import Channel, User
from flask_login import login_required
from ..sockets.views import get_channel_users

@api.route('/api/channels')
@login_required
def channel_list():
    channel_list = Channel.query.order_by(Channel.name).all()
    return {'channels': [{'name': channel.name, 'id': channel.id} for channel in channel_list]}

@api.route('/api/channel/<id>/users')
@login_required
def user_list(id):
    users = get_channel_users(id)
    usernames = []
    for user in users:
        usernames.append(user.username)
    return {'users': usernames}
