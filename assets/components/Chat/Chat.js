import React, {useState, useEffect} from 'react';
import propTypes from 'prop-types';
import Message from '../Message/Message';

const Chat = ({socket, activeChannel, pastMessages}) => {
    const [activeMessage, setActiveMessage] = useState('');

    const onMessageChange = (event) => {
        setActiveMessage(event.target.value);
    };

    const onMessageSend = (event) => {
        event.preventDefault();
        if (socket !== null) {
            const sendMessage = {
                type: 'message_channel', 
                body: activeMessage, 
                channel_id: activeChannel.id
            };
            socket.send(JSON.stringify(sendMessage));
            setActiveMessage('');
        }
    };

    let renderedMessages = [];
    for (const msg of pastMessages) {
        renderedMessages.push(<Message key={msg.id} message={msg} />);
    }
    return (
        <>
            <div className="row row-past-messages flex-grow-1 flex-column-reverse overflow-auto">
                <div className="col messages">
                    {renderedMessages}
                </div>
            </div>
            <div className="row chat-main w-100" >
                <div className="col message message-active">
                    <form onSubmit={onMessageSend}>
                        <input 
                            className="border text-light bg-dark border-dark rounded w-100" 
                            placeholder="Message..." 
                            type="text" 
                            value={activeMessage} 
                            onChange={onMessageChange} />
                    </form>
                </div>
            </div>
        </>
    );
}

Chat.propTypes = {
    socket: propTypes.instanceOf(WebSocket),
    activeChannel: propTypes.object,
    pastMessages: propTypes.array
}

export default Chat;
