import React from 'react';
import '../../index.css'

function Channel(props) {
    return (
        <div className='row row-channel'>
            <div className='col-sm col-channel'>
                <button className='text-light bg-dark channel-button' onClick={() => props.onClick()}>{props.name}</button>
            </div>
        </div>
    );
}

export default Channel;