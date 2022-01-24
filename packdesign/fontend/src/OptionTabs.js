import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';
import ReactDOM, { render } from 'react-dom';
import './OptionTabs.css';

import Slider from './components/Slider'
import ImageBlock from './components/ImageBlock'
import StyleTab from './StyleTab'

import img from './icons/magic-wand.png'
import StarIcon from './icons/icon-star.png'
import StyleIcon from './icons/icon-style.png'
import TempIcon from './icons/icon-temp.png'
import PicIcon from './icons/icon-pic.png'
import ColorIcon from './icons/icon-color.png'

/* ============ Tab Buttons ================= */
class TabBtn extends Component {
    render() {
        return (
            <div className='tab-btn-container' onClick={this.props.onClick}
            style={{backgroundColor:this.props.backgroundColor}} >
                <div className='tab-btn' >
                    <div className='image'>
                        <img src={this.props.icon}/>
                    </div>
                    <div className='text' style={{color:this.props.textColor, cursor:'default'}}>{this.props.value}</div>
                </div>
            </div>
        );
    }
}

/* ============ Tab Contents ================= */
class TabContent extends Component {
    static propTypes = {
        children: PropTypes.instanceOf(Array).isRequired
    }
    
    constructor(props) {
        super(props);

        this.state = {
            activeTab: this.props.children[0].props.tabName,
        };
    }

    handleOnClick = (tabName) => {
        this.setState({
            activeTab: tabName,
        });
    }

    render() {
        const items = this.props.children;
        return (
            <div className='option-operation-row'>
                <div className='option-btns'>
                    {items.map((item, idx)=>{
                        return (
                        <TabBtn 
                        key={idx} 
                        onClick={() => this.handleOnClick(item.props.tabName)} 
                        icon={item.props.icon} 
                        value={item.props.label} 
                        textColor={item.props.textColor}
                        backgroundColor={this.state.activeTab === item.props.tabName?'#162654':'transparent'}/>)
                    })}
                </div>
                <div className='option-console'>
                    {items.map((item, idx)=>{
                        return (<div key={idx} style={{display:this.state.activeTab===item.props.tabName?'':'none'}}>{item.props.children}</div>);
                    })}
                </div>
            </div>
        )
    }
}

class OptionTabs extends Component {
    constructor(props) {
        super(props);
                                                                                                                                                                                                                                                    
    }
    render() {
        return (
            <TabContent>

                <div icon={PicIcon} label='风格' textColor='white' tabName='console-style' >
                    <StyleTab model={this.props.model} onModelChange={this.props.onModelChange}/>
                </div>

                <div icon={StarIcon} label='主页' textColor='white' tabName='console-main'>
                    <Slider />
                    <input />
                </div>

                <div icon={TempIcon} label='样机' textColor='white' tabName='console-temp'>
                    <div style={{display:'flex', flexDirection:'row'}}>
                        <ImageBlock img={img} title='Block1' prompt='undifine'/>
                        <ImageBlock img={img} title='Block2' prompt='undifine' isPromptHover={false}/>
                    </div>
                </div>
                
                <div icon={StyleIcon} label='布局' textColor='white' tabName='console-layout'>
                    <div>Tab 3</div>
                </div>

                <div icon={ColorIcon} label='配色' textColor='white' tabName='console-color'>
                    <div>Hello World</div>
                </div>
            </TabContent>
        );
    }
}


export default OptionTabs