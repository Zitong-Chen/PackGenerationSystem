import React, {Component} from 'react';
import './OptionBtn.css';

class VerticalOptionBtn extends Component {

    render() {
        return (
            <div className='vertical-btn-container' onClick={this.props.onClick}
            style={{backgroundColor:this.props.backgroundColor}} >
                <div className='vertical-optionbtn' >
                    <div className='image'>
                        <img src={this.props.icon}/>
                    </div>
                    <div className='text' style={{color:this.props.textColor, cursor:'default'}}>{this.props.value}</div>
                </div>
            </div>
        );
    }
}

class HorizontalOptionBtn extends Component {
    render() {
        return (
            <div className='horizontal-btn-container' 
            onClick={this.props.onClick}
            style={{backgroundColor:this.props.backgroundColor,
            cursor:`${this.props.cursor}`}}>
                <div className='horizontal-optionbtn'>
                    <div className='image'>
                        <img src={this.props.icon}/>
                    </div>
                    <div className='text' style={{color:this.props.textColor,cursor:'default'}}>{this.props.value}</div>
                </div>
            </div>
        );
    }
}

export {VerticalOptionBtn, HorizontalOptionBtn};