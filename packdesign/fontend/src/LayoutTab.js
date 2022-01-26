import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';

import ImageBlock from './components/ImageBlock'
import UploadComponent from './components/UploadComponent';
import './LayoutTab.css'

import CameraIcon from './icons/camera.png'
import BlackIcon from './icons/black.jpg'

// =========== Layout Tab ===============
class LayoutTab extends Component {
    constructor(props) {
        super(props);
        this.state = {
            text: "",
            text_valid: false,
            prod: this.props.model.prod_url,
        }
    }

    handleInputChange = (e) => {
        var new_text = e.currentTarget.value;
        if (new_text.length > 5 || new_text.length < 1) {
            this.setState({
                text_valid: false,
            });
        } else {
            this.setState({
                text: new_text,
                text_valid: true,
            });
        };
    }

    handleUploadSuccess = (new_img_url, new_img_src) => {
        this.setState({
            prod: new_img_url,
        })
        this.props.model.prod_src = new_img_src;
        this.props.model.prod_url = new_img_url;
    }

    saveText = () => {
        this.props.model.text = this.state.text;
        this.forceUpdate();
    }


    render() {
        return (
            <div className='console-layout'>
                <div className='text-input'>
                    <span className='title'>短文字（1-5个字符）*</span>
                    <input type={'text'} onChange={this.handleInputChange}/>
                    <span style={{marginTop:'6px', fontSize:'10px', color:'red', 
                    display: this.state.text_valid ? 'none' : ''}}>注意：短文字应在1-5个字符</span> 
                    <span style={{color:'white', marginTop:'10px', marginRight:'10px',textDecoration:'underline',
                    fontSize:'12px', cursor:'pointer', textAlign:'right',display: this.state.text_valid ? '' : 'none'}} 
                    onClick={this.saveText}>保存</span>
                </div>

                <div style={{width:'100%',
                            height:'1px',
                            backgroundColor:'rgba(255,255,255,0.3)',
                            margin:"10px 0px"}}></div>

                <div className='prod-input'>
                    <span className='title'>产品图</span>
                    <div style={{display:'flex', alignItems:'center', flexDirection:'column'}}>
                        <UploadComponent icon={CameraIcon} text='点击上传照片' width='95%' 
                        height='100px' borderWidth='2px' borderStyle='dashed' textColor='white'
                        uploadUrl='/upload' preview={false} onUploadSuccess={this.handleUploadSuccess}/>
                    <span style={{marginTop:'2px', fontSize:'10px', color:'white',
                        display: this.state.prod === "" ? 'none' : ''}}>上传成功！</span>
                    </div>
                    
                </div>


                <div style={{width:'100%',
                            height:'1px',
                            backgroundColor:'rgba(255,255,255,0.3)',
                            margin:"10px 0px"}}></div>

                <div className='items-info' style={{display:'flex', flexDirection:'column'}}>
                    <span>素材信息</span>
                    <span style={{fontSize:'12px'}}>短文字：{this.props.model.text}</span>
                    <span style={{fontSize:'12px'}}>产品图：{this.props.model.prod_url}</span>
                </div>
            </div>
        );
    }
}

export default LayoutTab;