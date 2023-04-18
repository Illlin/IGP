import React, {Component} from "react";
import {AudioRecorderComponent as AudioRecorder} from "./AudioRecorder"
import errorModel from '../../Datastore/error.stl'
import placeHolderStl from '../../Datastore/WaitingForModel.stl'

export default class AudioComponent extends Component{  
   componentDidMount() {
   
    }   






    openFileExplorer = async () => {
        // Open file exp
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
            file.arrayBuffer().then((arrayBuffer) => {

                const blob = new Blob([new Uint8Array(arrayBuffer)], {type: file.type });
                
                this.postAudio(window.URL.createObjectURL(blob));

            }
            );
    
        }
        else{
            alert("Invalid file - only .wav accepted")
        }        
    }

 
    

    async postAudio(audioUrl) {
        const modelCallback = (stl) => {this.props.modelCallback(stl)}
        modelCallback(placeHolderStl);
              
        this.props.viewCallback();
              
        const apiUrl = '/api/sculpt';
        const formData = new FormData();
              
      
        try {
            const response = await fetch(audioUrl);
            const audioBlob = await response.blob();
            console.log("AUDIO DATA");
            console.log(audioBlob);
            // Append the Blob object to the FormData object
            formData.append('file', audioBlob, 'audio.wav');
            
            // Send the POST request with the FormData object
            const sculptResponse = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });
      
            const sculptData = await sculptResponse.json();
            console.log("Response Received");
            console.log(sculptData)
            modelCallback(sculptData["file"]);
        } catch (error) {
            console.log("There was an error");
            modelCallback(errorModel);        
        }   
    }

    render() {
        return (
            <div>
           
            {this.props.render===1 &&
             <div>
             <div className="headerSection">
                 <h1>AI Sound Sculpture Generator</h1>
            </div>
            <div className="text-box">
                <p>
                    This AI will allow you to record a 30 second description of a scene,
                    person, object. We will use the waveform image of the recording as the basis for the model
                    of our sculpture before using Watson Tone Analyser to analyse the voice recording the output of 
                    that analysis will provide an extra dimention to the sculpture. 
                </p>
            </div>


            <div id="primaryAudioContainer">
                <AudioRecorder 
                    id="audioRecorderComponent" 
                    parentCallback={this.handleCallbackSendAudio} 
                />

            <button className="main-page-button" id="uploadFileButton" onClick={this.openFileExplorer}>
                Chooose a file to upload
            </button>                         
            <p>File types accepted: .WAV</p>    
            </div>
            

           

            </div>
        
        }
        </div>

        );
    }
    handleCallbackSendAudio = (audioData) =>{

        this.postAudio(audioData);
    }    
}