import React, {Component, useState} from 'react';
import PropTypes from 'prop-types';

import ImageBlock from './components/ImageBlock'
import './MaterialTab.css'


class MaterialTab extends Component {
    constructor(props) {
        super(props);
        this.state = {
            layout_res:[],
            layout_state:false,
            color_res:[]
        }
    }

    handleOnLayoutGeneration = () => {
       

    } 

    handleOnColorGeneration = () => {

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
                            prompt='点击预览效果' onClick={() =>{ alert('click')}}/>
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
                            prompt='点击预览效果' onClick={() =>{ alert('click')}}/>
                        })}
                    </div>
                </div>
            </div>
        );
    }
}

export default MaterialTab;