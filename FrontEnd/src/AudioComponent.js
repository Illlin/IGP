import React, {Component} from "react";
import {AudioRecorderComponent} from "./AudioRecorderComponent"
import axios from "axios";

export default class AudioComponent extends Component{
    constructor(props) {
        super(props)
        this.state = {
            recorderStatus: "notRecorded",
            networkStatus:"noRequestMade",
            audioSrc: null,
        }
    }

    componentDidMount() {
    }   
   
    setRequest(status) {
        this.setState({
            networkStatus:status
        })
    }
    setModelState(status) {
        this.setState({
            modelRecievedForCurrentRecording:status
        })
    }

    setRecorder(status){
        this.setState({
            recorderStatus:status
        })
    }

    setAudioSrc(src){
        this.setState({
            audioSrc:src
        })
    }

    async postAudio(){
        const apiUrl = '/api/sculpt';
        const audioUrl = this.state.audioSrc;
        const formData = new FormData();
        
        fetch(audioUrl)
        .then(response => response.blob())
        .then(audioBlob => {
          // Append the Blob object to the FormData object
          formData.append('file', audioBlob, 'test_happy.wav');
      
          // Send the POST request with the FormData object
          return fetch(apiUrl, {
            method: 'POST',
            body: formData
          });
        })
        .then(response => {
          console.log(response.status);
          return response.json();
        })
        .then(data => {
          console.log(data);
        })
        .catch(error => {
          console.error(error);
        });
    }
               
    render() {
        return (
            <div id="primaryAudioContainer">

                {
                    this.state.recorderStatus==="audioError"&&
                    <p>Audio Error - Cannot Access Audio Device</p>
                }
                {
                    this.state.recorderStatus==="notRecorded"&&
                    <p>No Audio is Recorded</p>
                }
                {
                    this.state.recorderStatus==="audioRecording"&&
                    <p>Recording</p>
                }
                {
                    this.state.recorderStatus==="audioRecorded"&&
                    <p>Audio Recorded</p>
                }
            
        

                <AudioRecorderComponent 
                    id="audioRecorderComponent" 
                    parentCallback={this.handleCallbackSendAudio}
                    recordingCallback={this.handleCallbackIsRecording}
                    errorCallback={this.handleCallbackIsError}
                    >
                </AudioRecorderComponent>
                             
               

                {
                    (this.state.recorderStatus==="audioRecorded" && (this.state.networkStatus!=="requestSent")) &&
                    <button onClick={() => this.postAudio()}>Send to Server</button>
                }

                {this.state.recorderStatus==="audioRecorded" && 
                <button>
                    <a 
                        href={this.state.audioSrc}
                        download>
                        Download .WAV
                    </a>
                </ button>
}

                
                {
                  this.state.networkStatus==="noRequestMade" &&
                    <p>No HTTP Request Sent</p>
                }
                {
                    this.state.networkStatus==="requestSent" &&
                    <p>HTTP Request Sent</p>
                }
                {
                    this.state.networkStatus==="requestError" &&
                    <p>HTTP Request Error</p>
                }
                {
                    this.state.networkStatus==="responseRecieved" &&
                    <button >Send Audio to Server</button>
                }

            </div>

        );
    }
//    <audio controls autoPlay={true}     src={this.state.audioSrc}/>
    
    handleCallbackSendAudio = (childData) =>{
        this.setRecorder("audioRecorded");
        this.setAudioSrc(childData);
    }    

    handleCallbackIsRecording = () => {
        this.setState({recorderStatus:"audioRecording"})
    }
    handleCallbackIsError = () => {
        this.setState({recorderStatus:"audioError"})
    }
}