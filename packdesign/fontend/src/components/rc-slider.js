import Slider from 'rc-slider'
import 'rc-slider/assets/index.css';
import { Component } from 'react';
import './rc-slider.css'

export default class ControlSlider extends Component {
  constructor(props) {
    super(props);
    this.state = {
      value: 0,
    }
  }

  handlerOnChange = (value) => {
    this.setState({
      value: value,
    })
  }

  render() {
    return (
      <div className='control-slider' style={{color:this.props.color}}>
        {this.props.title && <span className='slider-title'>{this.props.title}</span>}
        <Slider className='slider-bar' 
        min={this.props.min} 
        max={this.props.max}
        onChange={this.handlerOnChange} 
        step={1} 
        handleStyle={{borderColor:'transparent'}}/>
        {this.props.percentage && <span className='slider-value'>{this.state.value}%</span>}
        {!this.props.percentage && <span className='slider-value'>{this.state.value}</span>}
      </div>
    );
  }
}