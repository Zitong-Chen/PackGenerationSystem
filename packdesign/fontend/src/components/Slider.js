import React, {Component, useState} from 'react';
import ReactDOM from 'react-dom';
import PropTypes from 'prop-types';
import './Slider.css';


class Slider extends Component {
    clientWidth = null;
    divWidth = null;
    maxBarWidth = null;
    startX = null;
    endX = null;

    static propTypes = {
        min: PropTypes.number,
        max: PropTypes.number,
        initialValue: PropTypes.number,
        handleChange: PropTypes.func,
        step: PropTypes.number,
        width: PropTypes.oneOfType([PropTypes.number, PropTypes.string]),
        diameter: PropTypes.number
    } 

    static defaultProps = {
        min: 0,
        max: 255,
        initialValue: 0,
        step: 1,
        width: '100%',
        diameter: 10,
    }

    constructor(props) {
        super(props);
        this.point = React.createRef();
        this.state = {
            value: 0,
        }
    }

    getClientWidth = () => {
        if (this.clientWidth == null) {
            const $root = ReactDOM.findDOMNode(this);
            this.clientWidth = $root.clientWidth;
        }
        return this.clientWidth;
    }

    getDivWidth = () => {
        if (this.clientWidth == null) {
            this.divWidth = this.getClientWidth() - Number(this.props.diameter);
        }
        return this.divWidth;
    }

    getMaxBarWidth = () => {
        if (this.maxBarWidth == null) {
            
            
        }
        const $point = ReactDOM.findDOMNode(this.point)
        console.log("Point Width:" + this.point.clientWidth);
        return "done";
    }

    getCoverLength = () => {
        let length = this.state.value <= this.getBarMaxWidth() ? this.state.value : this.getBarMaxWidth();
        console.log("Cover:"+length)
        return length;
    }

    getRepValue = () => {
        let repValue = this.state.value / this.getDivWidth() * (this.props.max - this.props.min);
        console.log("Rep" + repValue);
        return repValue;
    } 

    handleOnChange = value => {
        // console.log("Div:"+this.getMaxBarWidth());
        let newValue = this.state.value + Number(value);
        newValue = newValue <= this.getDivWidth() ? newValue : this.getDivWidth() ;
        newValue = newValue >= 0 ? newValue : 0;
        this.setState({
            value: newValue,
        });
        console.log(this.state.value);
    }

    render() {
        return (
            <div className='slider'>
                <div >
                    <span className='slider-title'>Title</span>
                </div>
                <div ref="main" className='slider-range' style={{width: this.getDivWidth}}>
                    <CoverBar clientWidth={this.getBarMaxWidth} coverLength={this.state.value} handleChange={this.handleOnChange} />
                    <Point clientWidth={this.getBarMaxWidth} handleChange={this.handleOnChange} diameter={this.props.diameter} ref={this.point}/>
                    <BaseBar clientWidth={this.getBarMaxWidth} handleChange={this.handleOnChange}/>
                 </div>
                <div >
                    <span className='slider-value'>{this.state.value}</span>
                </div>
            </div>
        );
    }

}

class Point extends Component {

    constructor(props) {
        super(props);
        console.log(props);
        
        this.state = {
            color: 'blue',
            pos: 0
        }
    }

    getCurrentPositionX = () => {
        // var $root = ReactDOM.findDOMNode(this);
        // )
        // this.getBoundingClientRect()
    }

    render() {
        return (
            <div className='point' 
            style={{backgroundColor:this.state.color,width:this.props.diameter,height:this.props.diameter}} 
            draggable={true}
            onMouseOver={this.handleOnMouseOver} 
            onMouseOut={this.handleOnMouseOut}
            onDrag={this.handleOnDrag}
            onDragOver={this.handleOnDragOver}></div>
        );
    }

    handleOnMouseOver = () => {
        // pointStyle.backgroundColor = 
        this.setState({
            color: 'white'
        });
    }

    handleOnMouseOut = () => {
        this.setState({
            color: 'blue'
        });
    }

    handleOnDrag = (e) => {
        let pointValue = e.clientX -  e.currentTarget.getBoundingClientRect().left;
        this.setState({
            pos: pointValue,
        });
        this.props.handleChange(pointValue);
        console.log("Point Change: " + pointValue)
    }

    // handleDragEnd = (e) => {

    // }

    handleOnDragOver = (e) => {
        e.preventDefault(); // ?

    }

    
    
} 

class BaseBar extends Component {
    render() {
        return (
            <div className='base-bar' onClick={this.handleOnClick}>
            </div>
        );
    }

    handleOnClick = (e) => {
        let diff = e.clientX -  e.currentTarget.getBoundingClientRect().left;
        this.props.handleChange(diff);
    }
}

class CoverBar extends Component {

    render() {
        return (
            <div className='cover-bar' 
            style={{width: this.props.coverLength}}
            onClick={this.handleOnClick}>
            </div>
        );
    }


    handleOnClick = (e) => {
        let diff = e.clientX -  e.currentTarget.getBoundingClientRect().right;
        this.props.handleChange(diff);
    }
}

export default Slider