import React, {Component} from "react";
import "../../App.css";
import AudioAnalyser from "react-audio-analyser"

export class AudioRecorderComponent extends Component {
    
    constructor(props) {
        super(props)
        this.state = {
            status: "inactive",
        }       
    }

    controlAudio(status) {this.setState({status})}

    sendAudioToParent = (data) => {
        this.props.parentCallback(data);
    }


    render() {     
        const {status, audioSrc,} = this.state;
        const audioType ="audio/wav";
        const backgroundColor="#a4dbe8";
        const audioProps = {
            backgroundColor,
            audioType,
            status,
            audioSrc,
            width:window.innerWidth*.8,
            height:window.innerHeight*.2,
            strokeColor:"#006699",
            timeslice: 1000, 

            startCallback: (e) => {
                console.log("Successful Audio Recording Started")
            },

            stopCallback: (e) => {
                this.setState({audioSrc: window.URL.createObjectURL(e)})
                console.log("Successful Audio recording Stopped");
                this.sendAudioToParent(window.URL.createObjectURL(e));
            },

            onRecordCallback: (e) => {
                console.log("Audio is Recording")
                
            },
            errorCallback: (err) => {
                this.controlAudio("inactive")
                console.log("Audio Callback Error", err)
                
                alert("Audio Recording Error, please check microphone permissions")

            }
        }
        return (
            <div>
                <AudioAnalyser {...audioProps} >
                    <div className="btn-box">

                        {status !== "recording" &&
                        <button className="main-page-button"
                           onClick={() => this.controlAudio("recording")}>Record Audio</button>}
                           
                        {status==="recording"&&
                        <button className="main-page-button" 
                           onClick={() => this.controlAudio("inactive")}>Stop Recording</button>}

                    </div>
                </AudioAnalyser>
            </div>
        );
    }
}