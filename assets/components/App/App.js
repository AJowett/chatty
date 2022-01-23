import React from 'react';
import Channel from '../Channel/Channel';
import Chat from '../Chat/Chat'
import '../../index.css'

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            channels: [],
            prevChannel: null,
            activeChannel: null,
            currentUsers: [],
        };

        fetch('/api/channels').then(res => res.json()).then(data => {
            this.setChannels(data.channels);
            this.setActiveChannel(data.channels[0]);
        });
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
                            <Chat activeChannel={this.state.activeChannel} setCurrentUsers={this.setCurrentUsers.bind(this)} />
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