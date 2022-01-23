import React, { useState } from 'react';
import moment from 'moment';

function Message(props) {
    return ( 
        <div className="message mt-1 mb-1">
            <div className="row g-0">
                <div className='col-2 profile-col'>
                    <img className='profile-thumbnail img-rounded img-thumbnail' src={props.message.profile}/>
                </div>
                <div className='col-8'>
                    <div className='row message-username'>
                        <div className='col-xs'>
                            <b>{props.message.username}</b>
                        </div>
                        <div className='col text-secondary'>
                            {moment(props.message.timestamp).format('h:mm a')}
                        </div>
                    </div>
                    <div className='row message-body'>
                        <div>
                            <p className='text-justify'>
                                {props.message.body}
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
     );
}

export default Message;