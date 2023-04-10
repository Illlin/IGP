import React, {Component} from "react";
import "../../App.css";
import {StlViewer} from "react-stl-viewer";

export class ModelViewComponent extends Component {

  componentDidMount() {
  }
 
  render() {

    const modelStyle = {
      width: '100vw',
      height: '100vh',
    };

    const modelProps={
      color:'#006699'
    }
    
    return (
      



      
      <div>
      {
        this.props.render===0 &&
        <div>
          <div className="headerSection">
            <h1>Your Sound Sculpture:</h1>
          </div>
          <div>
                  
            <StlViewer
            id='STLViewer'
            style={modelStyle}
            orbitControls
            shadows={true}
            modelProps={modelProps} 
            url={this.props.url}
            />

      <a href={this.props.url} onClick = {()=>this.props.viewCallback()}>
        <button id="download-button">
          Download .STL Model
        </button> </a> 
      </div>
      </div>
      }
    </div>
    );
  
}
}

