import React, { Component } from "react";
import { AudioRecorderComponent } from "./AudioRecorderComponent"

export default class AudioComponent extends Component {
    constructor(props) {
        super(props)
        this.state = {
            recorderStatus: "notRecorded",
            networkStatus: "noRequestMade",
            audioSrc: null,
        }
    }

    componentDidMount() {
    }

    setRequest(status) {
        this.setState({
            networkStatus: status
        })
    }
    setModelState(status) {
        this.setState({
            modelRecievedForCurrentRecording: status
        })
    }

    setRecorder(status) {
        this.setState({
            recorderStatus: status
        })
    }

    setAudioSrc(src) {
        this.setState({
            audioSrc: src
        })
    }

    async postAudio() {
        const apiUrl = '/api/sculpt';
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
                    body: formData
                });
            })
            .then(response => {
                console.log(response.status);
                return response.json();
            })
            .then(function (response) {
                console.log("Responce Recieved")
                this.setRequest("responseRecieved").bind(this);
            })
            .catch(function (error) {
                const x = "There was an error";
                console.log(x)
            });
    }

    render() {
        return (
            <div id="primaryAudioContainer">




                <AudioRecorderComponent
                    id="audioRecorderComponent"
                    parentCallback={this.handleCallbackSendAudio}
                    recordingCallback={this.handleCallbackIsRecording}
                    errorCallback={this.handleCallbackIsError}
                >
                </AudioRecorderComponent>



                {
                    (this.state.recorderStatus === "audioRecorded" && (this.state.networkStatus !== "requestSent")) &&
                    <button onClick={() => this.postAudio()}>Send to Server</button>
                }




            </div>

        );
    }
    //    <audio controls autoPlay={true}     src={this.state.audioSrc}/>

    handleCallbackSendAudio = (childData) => {
        this.setRecorder("audioRecorded");
        this.setAudioSrc(childData);
    }

    handleCallbackIsRecording = () => {
        this.setState({ recorderStatus: "audioRecording" })
    }
    handleCallbackIsError = () => {
        this.setState({ recorderStatus: "audioError" })
    }
}