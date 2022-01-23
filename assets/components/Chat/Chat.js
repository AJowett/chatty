import React, {useState, useEffect} from 'react';
import Message from '../Message/Message';

class Chat extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            activeMessage: '',
            pastMessages: [],
            activeChannel: null,
            prevChannel: null,
            socket: null,
        }
    }

  setActiveMessage(msg) {
      this.setState({
          activeMessage: msg,
      });
  }
  onMessageChange = (event) => {
    this.setActiveMessage(event.target.value);
  };

  onMessageSend = (event) => {
    event.preventDefault();
    if (this.state.socket !== null) {
      const messageBody = this.state.activeMessage;
      const sendMessage = {type: 'message', body: messageBody};
      this.state.socket.send(JSON.stringify(sendMessage));
      this.setActiveMessage('');
    }
  };

  onMessageRecv = event => {
    event.preventDefault();
    let recvMessage = JSON.parse(event.data);
    switch (recvMessage.type) {
        case 'message':
            this.setState({
                pastMessages: [...this.state.pastMessages, recvMessage]
            });
            break;
        case 'userlist':
            this.props.setCurrentUsers(recvMessage.users);
            break;
    }
  };

  setActiveChannel(channel) {
      this.setState({
          activeChannel: channel,
      });
  }

  setPrevChannel(channel) {
      this.setState({
          prevChannel: channel,
      });
  }

  setSocket(newSocket) {
      this.setState({
          socket: newSocket,
      });
  }

  componentDidUpdate() {
    //Changed Channel
    if (this.props.activeChannel !== null && this.props.activeChannel !== this.state.prevChannel) {
        let tempChannel = this.props.activeChannel;
        this.setActiveChannel(this.props.activeChannel);
        this.setPrevChannel(tempChannel);
        
        //Close socket connection for previous channel
        if (this.state.socket !== null) {
            let message = {type: 'close'};
            this.state.socket.send(JSON.stringify(message));
            this.state.socket.close();
            this.setSocket(null);
        }

        let tempSocket = new WebSocket('ws://' + window.location.host + '/channel/' + this.props.activeChannel.id);
        tempSocket.addEventListener('message', this.onMessageRecv);
        this.setSocket(tempSocket);

        this.setState({
            pastMessages: [],
        });
    }
  }

  render() {
    let renderedMessages = [];
    for (const msg of this.state.pastMessages) {
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
                    <form onSubmit={this.onMessageSend}>
                        <input 
                            className="border text-light bg-dark border-dark rounded w-100" 
                            placeholder="Message..." 
                            type="text" 
                            value={this.state.activeMessage} 
                            onChange={this.onMessageChange} />
                    </form>
                </div>
            </div>
        </>
    );
  }
}

export default Chat;
