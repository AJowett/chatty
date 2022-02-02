import React from 'react';
import Channel from '../Channel/Channel';
import Chat from '../Chat/Chat'
import '../../index.css'

class App extends React.Component {
    constructor(props) {
        super(props);

        // Create websocket connection
        let tempSocket = new WebSocket('ws://' + window.location.host + '/ws/chat');
        tempSocket.addEventListener('message', this.onMessageRecv);
        
        this.state = {
            channels: [],
            prevChannel: null,
            activeChannel: null,
            currentUsers: [],
            socket: tempSocket,
            pastMessages: [],
            channelMessages: {},
            directMessages: {},
        };   
        
        this.setUpChannels();
    }

    setUpChannels = () => {
        //Retrieve the list of channels
        fetch('/api/channels').then(res => res.json()).then(data => {
            //Retrieve past messages for each channel
            for (const channel of data.channels) {
                fetch('/api/channel/' + channel.id + '/messages').then(res => res.json()).then(data => {
                    //Merge the past messages with any received messages
                    let tempMessages = Object.assign({}, this.state.channelMessages);
                    if (tempMessages.hasOwnProperty(channel.id)) {
                        tempMessages[channel.id] = [...tempMessages[channel.id], ...data.messages];
                    } else {
                        tempMessages[channel.id] = data.messages;
                    }
                    this.setState({
                        channelMessages: tempMessages,
                    });
                });
            }
            this.setChannels(data.channels);
            this.setActiveChannel(data.channels[0]);
        });
    }

    onMessageRecv = (event) => {
        event.preventDefault();
        let recvMessage = JSON.parse(event.data);
        switch (recvMessage.type) {
            case 'message_channel':
                console.log("Received a message");
                
                let tempMessages = Object.assign({}, this.state.channelMessages);
                console.log("tempMessages: ", tempMessages);
                if (tempMessages.hasOwnProperty(recvMessage.channel_id)) {
                    tempMessages[recvMessage.channel_id] = [...tempMessages[recvMessage.channel_id], recvMessage];
                } else {
                    tempMessages[recvMessage.channel_id] = [recvMessage];
                }
                console.log("tempMessage: ", tempMessages);
                this.setState({
                    channelMessages: tempMessages,
                });
                console.log("channelMessages: ", this.state.channelMessages);
                break;
            case 'message_user':
                break;
            case 'user_list':
                this.setCurrentUsers(recvMessage.users);
                break;
        }
    }

    setChannels(newChannels) {
        this.setState({
            channels: newChannels
        });
    }

    setActiveChannel(channel) {
        let tempChannel = this.state.activeChannel;
        this.setState({
            activeChannel: channel,
            prevChannel: tempChannel,
        });
    }

    setCurrentUsers(users) {
        this.setState({
            currentUsers: users,
        });
    }

    componentDidMount() {
    }


    onChannelClick(channel) {
        this.setActiveChannel(channel);
    }

    render() {
        let renderedChannels = [];
        for (const channel of this.state.channels) {
            renderedChannels.push(<Channel 
                                key={channel.id} 
                                name={channel.name}
                                channelObj={channel}
                                onClick={() => this.onChannelClick(channel)} 
                            />);
        }

        let userList = [];
        for (const user of this.state.currentUsers.sort()) {
            userList.push(<div  key={user}>{user}</div>);
        }

        return (
            <main id="mainContent">
                <div className='main-container container-fluid chat-main mt-1 text-light bg-dark'>
                    <div className='row'>
                        <div className='col-2'>
                            Channels
                        </div>
                        <div className='col text-center'>
                            {this.state.activeChannel ? this.state.activeChannel.name : 'Chat'}
                        </div>
                        <div className='col-2 col-users pr-2'>
                            Users
                        </div>
                    </div>
                    <div className='row'>
                        <div className='col-2'>
                            {renderedChannels}
                        </div>
                        <div className='col chat-main-body'>
                            <Chat 
                                activeChannel={this.state.activeChannel} 
                                socket={this.state.socket} 
                                pastMessages={this.state.activeChannel !== null ? this.state.channelMessages[this.state.activeChannel.id] ?? [] : []} 
                            />
                        </div>
                        <div className='col-2 col-users pr-2 text-left'>
                            {userList}
                        </div>
                    </div>
                </div>
            </main>
        );
    }
}

export default App;