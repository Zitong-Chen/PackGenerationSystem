import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';

import ImageBlock from './components/ImageBlock'
import './MaterialTab.css'


class MaterialTab extends Component {
    constructor(props) {
        super(props);
        this.state = {
            layout_res: this.props.model.template_result,
            layout_state:false,
            color_res: this.props.model.color_result,
        }
    }
    handleOnLayoutGeneration = () => {
        if (this.props.model.select_background.length <= 0) {
            alert('请选择预览背景');
            return;
        }
        if (this.props.model.text.length <= 0) {
            alert('请上传短文字');
            return;
        }
        console.log('Start to generate template img...');
        let xhr = new XMLHttpRequest(); 
        let form = new FormData();
        form.append('backurl', this.props.model.select_background);
        form.append('text', this.props.model.text);
        form.append('prodBase64', this.props.model.prod_src)
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
                            layout_res: res_imgs,
                        }, () => {
                            this.props.model.template_result = this.state.layout_res;
                        }); 
                    } 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('POST', '/template', true);
        xhr.send(form);   
        console.log(this.state);

    } 

    handleOnColorGeneration = () => {
        if (this.props.model.select_background.length <= 0) {
            alert('请选择预览背景');
            return;
        }
        if (this.props.model.text.length <= 0) {
            alert('请上传短文字');
            return;
        }
        if (this.props.model.select_template.length <= 0) {
            alert('请选择预览布局');
            return;
        }
        console.log('Start to generate color img...');
        let xhr = new XMLHttpRequest(); 
        let form = new FormData();
        form.append('backurl', this.props.model.select_background);
        form.append('template', this.props.model.select_template)
        form.append('text', this.props.model.text);
        form.append('prodBase64', this.props.model.prod_src)
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
                            color_res: res_imgs,
                        }, () => {
                            this.props.model.color_result = this.state.color_res;
                        }); 
                    } 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('POST', '/color-decision', true);
        xhr.send(form);   
    } 

    handleOnTemplateClick = (new_img_src) => {
        console.log("New Source:"+new_img_src);
        this.props.model.select_template = new_img_src;
        this.props.model.img_src = new_img_src ;
        this.props.onModelChange();
    }

    handleOnColorClick = (new_img_src) => {
        console.log("New Source:"+new_img_src);
        this.props.model.img_src = new_img_src ;
        this.props.onModelChange();
    }

    render() {
        return (
            <div className='console-material'>
                <div className='layout-generation'>
                    <div style={{display: 'flex', flexDirection:'row', justifyContent:'space-between', alignContent:'center'}}>
                    <span>排版布局</span>
                    <span style={{textDecoration:'underline', fontSize:'12px', cursor:'pointer'}}
                    onClick={this.handleOnLayoutGeneration}>生成排版</span>
                    </div>
                    <div className='layout-result'>
                        {this.state.layout_res.map((layout_img, index) => {
                            return <ImageBlock key={index} img={layout_img} title={'布局'+(index+1)} 
                            prompt='点击选择及预览布局' onClick={() => this.handleOnTemplateClick(layout_img)}/>
                        })}
                    </div>
                </div>

                <div style={{width:'100%',
                            height:'1px',
                            backgroundColor:'rgba(255,255,255,0.3)',
                            margin:"10px 0px"}}></div>

                <div className='color-generation'>
                    <div style={{display: 'flex', flexDirection:'row', justifyContent:'space-between', alignContent:'center'}}>
                        <span>文字配色</span>
                        <span style={{textDecoration:'underline', fontSize:'12px', cursor:'pointer'}}
                        onClick={this.handleOnColorGeneration}>生成配色</span>
                    </div>
                    <div className='color-result'>
                        {this.state.color_res.map((color_img, index) => {
                            return <ImageBlock key={index} img={color_img} title={'配色'+(index+1)} 
                            prompt='点击预览效果' onClick={() => this.handleOnColorGeneration(color_img)}/>
                        })}
                    </div>
                </div>
            </div>
        );
    }
}

export default MaterialTab;