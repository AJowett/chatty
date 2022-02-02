from flask_login import login_required, current_user
from simple_websocket import ConnectionError, ConnectionClosed
from ..models import User, Channel, Message
from .. import sock, db
from datetime import datetime
import json
import uuid

## Set of the form:
## {user_id: ws, user_id2: ws2}
## where ws is the websocket connection and 
## user_id is the id of the connected user
users = {}

@sock.route('/ws/chat')
@login_required
def chat(ws):
    ## Login
    print("Connected...")
    users[current_user.id] = ws
    update_user_list()

    
    while True:
        try:
            raw_data = ws.receive()
        except ConnectionClosed:
            print("WEBSOCKET CONNECTION CLOSED")
            users.pop(current_user.id)
            update_user_list()
            break
        except ConnectionError:
            print("WEBSOCK CONNECTION ERROR")
            users.pop(current_user.id)
            update_user_list()
            break

        try:
            data = json.loads(raw_data)
        except Exception as e:
            print("Invalid message")
            data = {'type': 'error'}
        
        print('Data: ', data)
        match data['type']:
            case "logout":
                ## Disconnecting
                print('logout')
            case "message_channel":
                ## Sending a message to a channel
                body = data['body'].strip()
                channel_id = data['channel_id']
                print('channel_id: ', channel_id)
                channel = Channel.query.filter_by(id=channel_id).first()
                print('channel: ', channel)
                if body != '' and channel != None:
                    message = Message(body=body, author=current_user._get_current_object(), channel=channel)
                    db.session.add(message)
                    db.session.commit()
                    response = {"type": "message_channel", 
                                "id": str(message.id),
                                "channel_id": message.channel_id, 
                                "username": current_user.username, 
                                "timestamp": str(message.timestamp),
                                "profile": current_user.gravatar(),
                                "body": message.body}
                    message_all_users(response)
                print('message_channel')

            case "message_user":
                ## Sending a message to a user
                print('message_channel')
            case "error":
                ## error occured in parsing command
                print('error')

            case _:
                ## Unrecognized command
                print('unrecognized command')

def message_all_users(message):
    """Sends a message to all users

    :param message: The message to send (will be JSON)
    :type message: Disctionary
    """
    print("message: ", message)
    print("users: ", users.keys())
    for user_id in users.keys():
        try:
            users[user_id].send(json.dumps(message))
        except:
            continue

def get_online_users():
    """Returns a list of all the connected users

    :return: All connected users
    :rtype: List of user objects
    """
    all_users = []
    for user_id in users.keys():
        user = User.query.filter_by(id=user_id).first()
        all_users.append(user)
    return all_users

def update_user_list():
    """Sends the list of online users to online users
    """
    data = {"type": "user_list"}
    usernames = [user.username for user in get_online_users()]
    data["users"] = usernames
    for user_id in users.keys():
        try:
            users[user_id].send(json.dumps(data))
        except:
            continue

def message_user(username, message):
    """Sends a message to a single user

    :param username: The user to message
    :type username: string
    :param message: The message to send (will be JSON)
    :type message: Dictionary
    """
    recv_user = User.query.filter_by(username=username).first()
    connection = users[recv_user.id]
    try:
        connection.send(json.dumps(message))
    except ConnectionClosed:
        pass
    except ConnectionError:
        pass
    return