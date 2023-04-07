import React, {Component} from "react";
import "../../App.css";
import {StlViewer} from "react-stl-viewer";

export class ModelViewComponent extends Component {

  componentDidMount() {
  }
 
  render() {

    const modelStyle = {
      width: '100vw',
      height: '60vh',
    };

    const modelProps={
      color:'white'
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

          <button >
            <a href={this.props.url} onClick = {()=>this.props.viewCallback()}>Download</a>
          </button>  
      </div>
      </div>
      }
    </div>
    );
  
}
}

