import React, {Component} from 'react';
import ImageBlock from './ImageBlock';

import './UploadComponent.css'

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
                        upload_img: data.url,
                        upload_img_src: data.img,
                    }, () => this.setUploadState(true)); 
                }
            }
            else {
                // console.log(xhr.responseText);
            }
        }
        xhr.open('POST', this.props.uploadUrl, true);
        xhr.send(form); 
    }

    setUploadState = (uploadState) => {
        this.setState({
            uploaded: uploadState
        })
        if (this.props.onUploadSuccess) {
            console.log(this.state.upload_img);
            this.props.onUploadSuccess(this.state.upload_img, this.state.upload_img_src);
        }
    }

    render() {
        return (
            <div style={{display:'flex', flexDirection:'column', alignItems:'center',width:`${this.props.width}`}}>
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
                    <div style={{width:'100%', margin:'0px'}}>
                        <div className='upload-info'>
                            <span className='file-name'>{this.state.upload_file}</span>
                            <span className='upload-btn' onClick={this.handleUpload}>上传</span>
                        </div>
                        { this.props.preview && this.state.uploaded &&
                        <div className='upload-preview' style={{marginTop:'15px', display:'flex', justifyContent:'center'}}>
                        
                            <div style={{display:'flex', justifyContent:'right', width:'100%'}}>
                                <ImageBlock title='上传图片' prompt='点击预览效果' img={this.state.upload_img} 
                                onClick={() => this.props.onPreviewImageClick(this.state.upload_img)}/>
                            </div>
                        
                        </div>
                        }
                    </div>
                }
            </div>
            
        );
    }
}

export default UploadComponent;