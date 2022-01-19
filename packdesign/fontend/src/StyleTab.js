import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';

// import Slider, {Range} from 'rc-slider'
// import 'rc-slider/assets/index.css';

import ControlSlider from './components/rc-slider';

import ImageBlock from './components/ImageBlock'
import './StyleTab.css'

import CameraIcon from './icons/camera.png'

// import styled from 'styled-components';


/* ============ Upload Component ============== */
class UploadComponent extends Component {
    render() {
        return (
            <div className='upload-box' 
            style={{height:this.props.height, 
            width:this.props.width, 
            borderWidth:this.props.borderWidth,
            borderStyle:this.props.borderStyle,
            color:this.props.textColor,
            }}
            onClick={this.props.onClick}>
                <img src={this.props.icon}/>
                <span>{this.props.text}</span>
            </div>
        );
    }
}

/* ============ Style Buttons ================= */
class StyleBtn extends Component {
    render() {
        return (
            <div className='style-btn-container' onClick={this.props.onClick}
            style={{backgroundColor:this.props.backgroundColor}} >
                <div className='style-btn' >
                    <div className='text' style={{color:this.props.textColor, cursor:'default'}}>{this.props.value}</div>
                </div>
            </div>
        );
    }
}

/* ============ Tab Buttons ================= */
class TabBtn extends Component {
    render() {
        return (
            <div className='style-tab-btn-container' onClick={this.props.onClick}
            style={{backgroundColor:this.props.backgroundColor}} >
                <div className='style-tab-btn' >
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
            <div className='console-style'>
                <div className='style-tab-btns'>
                    {items.map((item, idx)=>{
                        return (
                        <TabBtn 
                        key={idx} 
                        onClick={() => this.handleOnClick(item.props.tabName)} 
                        value={item.props.label} 
                        textColor={item.props.textColor}
                        backgroundColor={this.state.activeTab === item.props.tabName?'#2f437e':'#1d3068'}/>)
                    })}
                </div>
                <div className='style-tab-contents'>
                    {items.map((item, idx)=>{
                        return (<div className={item.props.className} 
                            key={idx} 
                            style={{display:this.state.activeTab===item.props.tabName?'':'none'}}>{item.props.children}</div>);
                    })}
                </div>
            </div>
        )
    }
}

class StyleTab extends Component {
    generateDesign = style => {
        console.log('Start to generate style imgs...');
        let xhr = new XMLHttpRequest(); 
        xhr.onreadystatechange = () => {
            // 根据服务器的响应内容格式处理响应结果
            if (xhr.readyState === 4 && xhr.status === 200) {
                if(xhr.getResponseHeader('content-type')==='application/json'){
                    var res_imgs = [];
                    let data = JSON.parse(xhr.responseText);
                    let imgs = data.img;
                    let base_dir = data.base_dir;

                    for(let i = 0; i < imgs.length; ++i) {
                        res_imgs.push(base_dir+imgs[i]);
                    }
                    this.setState({
                        style:style,
                        style_imgs:res_imgs,
                    }); 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('GET', '/generate', true);
        xhr.send(null);   
        console.log(this.state);
    }

    constructor(props) {
        super(props);
        this.state = {
            style: 1,
            style_imgs: ['./icons/camera.png'],
        };
    }

    render() {
        return (
            <TabContent>
                <div label='纯色背景' textColor='white' tabName='color-style' className='color-style-control'>
                    <div style={{display:'flex', flexDirection:'column'}} >
                        <div className='r-channel'>
                            {/* <span style={{color:'white'}}>R通道</span> */}
                            <ControlSlider min={0} max={255} color='white' title='R通道' percentage={false}/>

                        </div>
                        <div className='g-channel'>
                            {/* <span style={{color:'white'}}>G通道</span> */}
                            <ControlSlider min={0} max={255} color='white' title='G通道' percentage={false}/>

                        </div>
                        <div className='b-channel'>
                            {/* <span style={{color:'white'}}>B通道</span> */}
                            <ControlSlider min={0} max={255} color='white' title='B通道' percentage={false}/>

                        </div>
                    </div>
                </div>

                <div label='智能生成' textColor='white' tabName='gan-style' className='gan-style-control'>
                    <div style={{display:'flex', flexDirection:'column'}} >
                        
                            <span style={{color:'white'}}>风格选择</span>
                            <div className='style-btns'>
                                <StyleBtn value='风格1' textColor='white' backgroundColor='#1d3068' onClick={()=>this.generateDesign(1)}/>
                                <StyleBtn value='风格2' textColor='white' backgroundColor='#1d3068' onClick={()=>this.generateDesign(2)} />

                            </div>
                            <div className='style-generate'>
                                <div className='generate-img-block' >
                                    {
                                    this.state.style_imgs.map((style_img, index) => {
                                        return <ImageBlock key={index} img={style_img} title='text' prompt='text2'/>
                                    })
                                    }
                                </div>
                            </div>
                            <div style={{width:'100%',
                            height:'1px',
                            backgroundColor:'rgba(255,255,255,0.3)',
                            marginBottom:"25px"}}></div>
                            <span style={{color:'white'}}>风格细调</span>
                            <div className='style-adjust'>
                                <ControlSlider min={0} max={100} color='white' title='模糊' percentage={true}/>
                                <ControlSlider min={0} max={100} color='white' title='抽象' percentage={true}/>
                                <ControlSlider min={0} max={100} color='white' title='颗粒大小' percentage={true}/>
                                <ControlSlider min={0} max={100} color='white' title='透明' percentage={true}/>
                            </div>
                        
                    </div>
                </div>

                <div label='本地上传' textColor='white' tabName='upload-style' className='upload-style-control'>
                    <UploadComponent icon={CameraIcon} text='点击上传照片' width='90%' 
                    height='100px' borderWidth='2px' borderStyle='dashed' textColor='white'
                    onClick={() => {alert("upload img")}}/>
                </div>

            </TabContent>
        )
    }
}

export default StyleTab;