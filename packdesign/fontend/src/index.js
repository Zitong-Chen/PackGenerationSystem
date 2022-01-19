import React, {Component, useState} from 'react';
import ReactDOM, { render } from 'react-dom';
// import Slider from 'react-native'
import './index.css';
import {VerticalOptionBtn, HorizontalOptionBtn} from './components/OptionBtn'
import ImageContainer from './components/ImageContainer'
import OptionTabs from './OptionTabs'

import MagicIcon from './icons/line-magic.png'
import FolderIcon from './icons/folder.png'
import BoxIcon from './icons/icon-box.png'

  
function click() {
  alert('click');
}



/* ============ Option Head ================= */
function OptionHead(props) {
  return (
    <div className='option-header'>
      {/* <img src={img} onClick={() => click()} />
      <img src={img} /> */}
      <img src={BoxIcon}></img>
      <span>智绘包装</span>
    </div>
  );
}


/* ============ Option Footer ================= */
function OptionFooter(props) {
  return (
    <div className='option-footer'>
      <div className='option-footer-1' style={{cursor:'pointer', width:'50%'}}>
        <HorizontalOptionBtn onClick={click} icon={MagicIcon} value='收藏作品'/>
      </div>
      <div className='option-footer-2' style={{cursor:'pointer', width:'50%'}}>
        <HorizontalOptionBtn onClick={click} icon={FolderIcon} value='打开文件'/>
      </div>
    </div>
  );
}

/* ============ Display Header ================= */
function DisplayHeader(props) {
  return (
    <div className='display-header'>
      {/* <HorizontalOptionBtn onClick={click} icon={img} value='back'/>
      <HorizontalOptionBtn onClick={click} icon={img} value='next'/> */}
      <span style={{color:'lightgray'}}>展示台</span>
    </div>
  );
}

/* ============ Display Container ================= */
function DisplayContainer(props) {
  return (
    <div className='display-container'>
        <ImageContainer  img={BoxIcon}/>
    </div>
  );
}

/* ============== Main Page =============== */
function Body() {
  return (
    <div className='page'>
      <div className='option-column'>
        <OptionHead />
        <OptionTabs />
        <OptionFooter />
      </div>
      <div className='display-column'>
        <DisplayHeader />
        <DisplayContainer />
      </div>
    </div>

  );
}

ReactDOM.render(
  <Body />,
  document.getElementById('root')
);
  