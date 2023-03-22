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
        const audioData = this.state.audioSrc;
        const formData = new FormData();
        formData.append("audio", audioData);

        this.setRequest("requestSent")
        axios.post(apiUrl, formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
        })
        .then(function (response) {
            console.log("Responce Recieved")
            this.setRequest("responseRecieved").bind(this);
        })
        .catch(function (error) {
            const  x ="There was an error";
            console.log(x)
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