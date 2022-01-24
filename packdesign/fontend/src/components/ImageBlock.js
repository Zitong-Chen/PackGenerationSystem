import React, {Component} from 'react';
import ReactDOM from 'react-dom'
import './ImageBlock.css'

class ImageBlock extends Component {
    constructor (props) {
        super(props);
        this.state = {
            isHover: false,
            isPromptHover: this.props.isPromptHover == null ? true : this.props.isPromptHover,
        }
    }

    handleOnMouseEnter = (e) => {
        let blockLeft = e.currentTarget.getBoundingClientRect().left;
        let blockRight = e.currentTarget.getBoundingClientRect().right;
        let blockTop = e.currentTarget.getBoundingClientRect().top;
        let blockBottom = e.currentTarget.getBoundingClientRect().bottom;

        this.setState({
            isHover: true,
            left: blockLeft + 'px',
            right: blockRight + 'px',
            top:  blockTop + 'px',
            bottom: blockBottom + 'px',
        })
    }

    handleOnMouseLeave = (e) => {
        this.setState({
            isHover: false,
        })
    }


    render() {
        return (
            <div style={{display:'flex', flexDirection:'column'}}
                onMouseEnter={this.handleOnMouseEnter}
                onMouseLeave={this.handleOnMouseLeave}
                onClick={this.props.onClick}>
                <div className='img-block' style={this.props.style}>
                    <img src={this.props.img}/>
                    { this.state.isPromptHover && this.state.isHover &&
                        <div className='hover-text' style={{left:`${this.state.left}`, top:`${this.state.top}`}}>
                            <span className='title'>{this.props.title}</span>
                            <span className='prompt'>{this.props.prompt}</span>
                        </div>
                    }
                </div>
                {  !this.state.isPromptHover && this.state.isHover && 
                    <InfoCard top={this.state.top} left={this.state.right}
                    title={this.props.title} prompt={this.props.prompt}/>
                }
            </div>
        );
    }
}


class InfoCard extends Component {


    render() {
        return (
            <div className='info-card'
            style={{top:this.props.top, left:this.props.left}}>
                <div className='hover-text' >
                    <span className='title'>{this.props.title}</span>
                    <span className='prompt'>{this.props.prompt}</span>
                </div>
            </div>
        )
    }
}

export default ImageBlock