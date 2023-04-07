import React, {Component} from "react";
import {AudioRecorderComponent as AudioRecorder} from "./AudioRecorder"
import errorModel from '../../Datastore/error.stl'
import placeHolderStl from '../../Datastore/WaitingForModel.stl'

export default class AudioComponent extends Component{  
   
    constructor(props) {
        super(props)
        this.state = {
            audioSrc: null,
        }
    }

    componentDidMount() {
    }   


    setAudioSrc(src){
        this.setState({
            audioSrc:src
        })
    }



    openFileExplorer = async () => {
        // Open file exp
        console.log(this.state)
        const pickerProps = {
            types: [{
                description: "Audio",
                accept: {"audio/*": [".wav",]}
            }],
            excludeAcceptAllOption: false,
            multiple: false,
          };
          
        const [fileHandle] = await window.showOpenFilePicker(pickerProps);
        const file = await fileHandle.getFile();
    
        if (file.type==="audio/wav"){
            this.setAudioSrc(file.text);
            this.postAudio();
        }
        else{
            alert("Invalid file - only .wav accepted")
        }        
    }

 
    

    async postAudio(){
        const modelCallback = (stl) => {this.props.modelCallback(stl)}
        modelCallback(placeHolderStl);
        this.props.viewCallback();
        const apiUrl = 'http://127.0.0.1:5000/api/sculpt';
        const audioUrl = this.state.audioSrc;
        const formData = new FormData();
        
        fetch(audioUrl)
        .then(response => response.blob())
        .then(audioBlob => {
          // Append the Blob object to the FormData object
          formData.append('file', audioBlob, 'audio.wav');
      
          // Send the POST request with the FormData object
        return fetch(apiUrl, {
            method: 'POST',
            body: formData,
            mode:"no-cors",}
        );})

        .then(response => {
        console.log(response.status);
          return response.json();
        })
        .then(function (response) {
            console.log("Responce Recieved")
            this.setRequest("responseRecieved").bind(this);
            modelCallback(response);

        })
        .catch(function (error) {
            console.log("There was an error");
            modelCallback(errorModel);        
        });    
    }

    render() {
        return (
            <div>
           
            {this.props.render===1 &&
             <div>
             <div className="headerSection">
                 <h1>AI Sound Sculpture Generator</h1>
            </div>
            
            <div id="primaryAudioContainer">
                <AudioRecorder 
                    id="audioRecorderComponent" 
                    parentCallback={this.handleCallbackSendAudio} 
                />

            <button id="uploadFileButton" onClick={this.openFileExplorer}>
                Chooose a file to upload
            </button>                         
                
            </div>
            

            </div>
        
        }
        </div>

        );
    }
    handleCallbackSendAudio = (audioData) =>{
        this.setAudioSrc(audioData);
        this.postAudio();
    }    

    

//    handleCallbackIsRecording = () => {
//        this.setState({recorderStatus:"audioRecording"})
//    }
//    handleCallbackIsError = () => {
//        this.setState({recorderStatus:"audioError"})
//    }
}