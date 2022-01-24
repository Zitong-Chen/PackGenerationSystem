import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';

// import Slider, {Range} from 'rc-slider'
// import 'rc-slider/assets/index.css';

import ControlSlider from './components/rc-slider';

import ImageBlock from './components/ImageBlock'
import './StyleTab.css'

import CameraIcon from './icons/camera.png'
import BlackIcon from './icons/black.jpg'


// import styled from 'styled-components';


/* ============ Upload Component ============== */
class UploadComponent extends Component {
    constructor(props) {
        super(props);
        this.state = {
            readyUpload: false,
            uploaded: false,
            upload_file: null,
            target_file: null,
        }
        this.input = React.createRef();
    }

    handleOnClick = () => {
        this.input.current.click();
    }

    handleOnChange = (event) => {
        let files = event.target.files;
        if (files.length === 1) {
            this.setState({
                readyUpload: true,
                upload_file: files[0].name,
                target_file: files[0]
            });
        }
    }

    handleUpload = () => {
        console.log('Start to upload img...');
        let xhr = new XMLHttpRequest(); 
        let form = new FormData();
        form.append('file', this.state.target_file);
        xhr.onreadystatechange = () => {
            // 根据服务器的响应内容格式处理响应结果
            if (xhr.readyState === 4 && xhr.status === 200) {
                if(xhr.getResponseHeader('content-type')==='application/json'){
                    let data = JSON.parse(xhr.responseText);
                    this.setState({
                        upload_img: data.img,
                    }, this.setUploadState(true)); 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('POST', '/upload', true);
        xhr.send(form); 
    }

    setUploadState = (uploadState) => {
        this.setState({
            uploaded: uploadState
        })
    }

    render() {
        return (
            <div style={{display:'flex', flexDirection:'column', 
            alignItems:'center',width:`${this.props.width}`}}>
                <div>
                    <input type='file' accept='.jpg,.png,.jpge' multiple={false} style={{opacity:0}}
                    width='100%' ref={this.input} onChange={this.handleOnChange}></input>
                </div>
                <div className='upload-box' 
                    style={{height:this.props.height, 
                    borderWidth:this.props.borderWidth,
                    borderStyle:this.props.borderStyle,
                    color:this.props.textColor,
                    }}
                    onClick={this.handleOnClick}>
                    <img src={this.props.icon}/>
                    <span>{this.props.text}</span>
                </div>
                {   this.state.readyUpload && 
                    <div style={{width:'100%'}}>
                        <div className='upload-info'>
                            <span className='file-name'>{this.state.upload_file}</span>
                            <span className='upload-btn' onClick={this.handleUpload}>上传</span>
                        </div>
                        <div className='upload-preview' style={{marginTop:'15px', display:'flex', justifyContent:'center'}}>
                        </div>
                    </div>
                }
                {
                    this.state.uploaded &&
                    <div style={{display:'flex', justifyContent:'right', width:'100%'}}>
                        <ImageBlock title='上传图片' prompt='点击预览效果' img={this.state.upload_img} 
                        onClick={() => this.props.onImageClick(this.state.upload_img)}/>
                    </div>
                }
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
    constructor(props) {
        super(props);
        this.state = {
            style: 1,
            style_imgs: [],
            R: 0,
            G: 0,
            B: 0,
            color_img: BlackIcon,
            upload_img: CameraIcon,
        };
    }

    generateDesign = style => {
        console.log('Start to generate style imgs...');
        let xhr = new XMLHttpRequest(); 
        xhr.onreadystatechange = () => {
            // 根据服务器的响应内容格式处理响应结果
            if (xhr.readyState === 4 && xhr.status === 200) {
                if(xhr.getResponseHeader('content-type')==='application/json'){
                    var res_imgs = [];
                    let data = JSON.parse(xhr.responseText);
                    let status = data.status;
                    if (status) {
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
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('GET', '/generate/style='+style, true);
        xhr.send(null);   
    }

    generateColorImg = () => {
        console.log('Start to generate single color img...');
        let xhr = new XMLHttpRequest(); 
        let form = new FormData();
        form.append('R', this.state.R);
        form.append('G', this.state.G);
        form.append('B', this.state.B);
        xhr.onreadystatechange = () => {
            // 根据服务器的响应内容格式处理响应结果
            if (xhr.readyState === 4 && xhr.status === 200) {
                if(xhr.getResponseHeader('content-type')==='application/json'){
                    let data = JSON.parse(xhr.responseText);
                    let img = data.img;
                    let base_dir = data.base_dir;

                    this.setState({
                        color_img: base_dir+img,
                    }); 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('POST', '/single-color', true);
        xhr.send(form);   
        console.log(this.state);
    }

    handleChange_R = (new_R) => {
        console.log("New R:", new_R);
        this.setState({
            R: new_R,
        }, () => {
            console.log("New State:", this.state);
            this.props.model.single_color_R = new_R;
            this.generateColorImg();
        });
    }

    handleChange_G = (new_G) => {
        this.setState({
            G: new_G,
        }, () => {
            this.props.model.single_color_G = new_G;
            this.generateColorImg();
        });
    }

    handleChange_B = (new_B) => {
        this.setState({
            B: new_B,
        }, () => {
            this.props.model.single_color_B = new_B;
            this.generateColorImg();
        });
    }

    onImageClick = (new_img_src) => {
        console.log("New Source:"+new_img_src);
        this.props.model.img_src = new_img_src ;
        this.props.onModelChange();
    }

    upload_img = () => {

    }

    render() {
        return (
            <TabContent>
                <div label='纯色背景' textColor='white' tabName='color-style' className='color-style-control'>
                    <div style={{display:'flex', flexDirection:'column'}} >
                        <div className='r-channel'>
                            <ControlSlider min={0} max={255} color='white' title='R通道' 
                            percentage={false} handleChangeValue={this.handleChange_R}/>

                        </div>
                        <div className='g-channel'>
                            <ControlSlider min={0} max={255} color='white' title='G通道' 
                            percentage={false}  handleChangeValue={this.handleChange_G}/>

                        </div>
                        <div className='b-channel'>
                            <ControlSlider min={0} max={255} color='white' title='B通道' 
                            percentage={false}  handleChangeValue={this.handleChange_B}/>
                        </div>
                        <div className='color-preview' style={{marginTop:'15px', marginRight:'20px', 
                        display:'flex', justifyContent:'right'}}>
                            <ImageBlock title='纯色图片' prompt='点击预览效果' img={this.state.color_img} 
                            onClick={() => this.onImageClick(this.state.color_img)}/>
                        </div>
                    </div>
                </div>

                <div label='智能生成' textColor='white' tabName='gan-style' className='gan-style-control'>
                    <div style={{display:'flex', flexDirection:'column'}} >
                        
                            <span style={{color:'white'}}>风格选择</span>
                            <div className='style-btns'>
                                <StyleBtn value='渲染' textColor='white' backgroundColor='#1d3068' onClick={()=>this.generateDesign(1)}/>
                                <StyleBtn value='抽象' textColor='white' backgroundColor='#1d3068' onClick={()=>this.generateDesign(2)} />

                            </div>
                            <div className='style-generate'>
                                <div className='generate-img-block' >
                                    {
                                    this.state.style_imgs.map((style_img, index) => {
                                        return <ImageBlock key={index} img={style_img} title={'生成图片'+(index+1)} 
                                        prompt='点击预览效果' onClick={() => this.onImageClick(style_img)}/>
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
                    onImageClick={this.onImageClick}/>
                </div>

            </TabContent>
        )
    }
}

export default StyleTab;