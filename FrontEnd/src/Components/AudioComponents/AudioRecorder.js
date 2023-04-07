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
//
//    componentDidMount() {
//    }
//
    controlAudio(status) {this.setState({status})}

//    setIsRecording = () =>{
//        this.props.recordingCallback();
//    }

//    setIsError = () =>{
//            this.props.errorCallback();
//            
//        }
    sendAudioToParent = (data) => {
        this.props.parentCallback(data);
    }


    render() {     
        const {status, audioSrc,} = this.state;
        const audioType ="audio/wav";
        const backgroundColor="#282c34";
        const audioProps = {
            backgroundColor,
            audioType,
            status,
            audioSrc,
            width:300,
            height:100,
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
  //              this.setIsRecording()
                console.log("Audio is Recording")
                
            },
            errorCallback: (err) => {
   //             this.setIsError()
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
                        <button className="startRecordingButton" 
                           onClick={() => this.controlAudio("recording")}>Record Audio</button>}
                           
                        {status==="recording"&&
                        <button className="stopRecordingButton" 
                           onClick={() => this.controlAudio("inactive")}>Stop Recording</button>}

                    </div>
                </AudioAnalyser>
            </div>
        );
    }
}