import React, {Component} from 'react';
import './ImageContainer.css';

class ImageContainer extends Component {
    render() {
        return (
            <div className='img-container'>
                <img src={this.props.img}/>
            </div>
        );
    }
}

export default ImageContainer
