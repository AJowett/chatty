from flask_login import login_required, current_user
from simple_websocket import ConnectionError, ConnectionClosed
from ..models import User, Channel, Message
from .. import sock
from datetime import datetime
import json
import uuid

channels = {}

@sock.route('/channel/<id>')
@login_required
def channel(ws, id):
    ## Connecting to new channel
    if id not in channels:
        channels[id] = set([])
    
    ## New user joining channel
    if (ws, current_user.id) not in channels[id]:
        channels[id].add((ws, current_user.id))
        update_user_list(id)

    while True:
        data = json.loads(ws.receive())
        data_type = data.get('type')
        if data_type == "message":
            data['timestamp'] = str(datetime.now())
            data['id'] = str(uuid.uuid4())
            data['username'] = current_user.username
            data['profile'] = current_user.gravatar()
        elif data_type == "close":
            channels[id].remove((ws, current_user.id))
            update_user_list(id)
            return
        
        message_channel(id, data)
        update_user_list(id)
        
def message_channel(channel_id, message):
    """Sends a message to all users in the specified channel

    :param channel_id: The integer id of the channel to message
    :type channel_id: int
    :param message: [description]
    :type message: [type]
    """
    connections = channels[channel_id]
    closed_connections = set([])
    for connection in connections:
        try:
            connection[0].send(json.dumps(message))
        except ConnectionClosed:
            print("Connection closed...")
            closed_connections.add(connection)
        except ConnectionError:
            print("Connection error...")
            closed_connections.add(connection)
        except Exception as e:
            print("Other exception...")
            print(e)

    if len(closed_connections) != 0:
        channels[channel_id] = connections.difference(closed_connections)

def get_channel_users(channel_id):
    users = []
    if channel_id in channels:
        ping = {'type': 'ping'}
        message_channel(channel_id, ping)
        connections = channels[channel_id]
        unique_ids = set([])
        for connection in connections:
            user_id = connection[1]
            if user_id not in unique_ids:
                user = User.query.filter_by(id=user_id).first()
                users.append(user)
    return users

def update_user_list(channel_id):
    data = {'type': 'userlist'}
    usernames = []
    for user in get_channel_users(channel_id):
        usernames.append(user.username)
    data['users'] = usernames
    message_channel(channel_id, data)        