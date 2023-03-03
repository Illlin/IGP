import React from 'react';
import ReactDOM from 'react-dom';
import {StlViewer} from "react-stl-viewer";
import logo from './logo.png';
import './App.css';
import svg from './Datastore/Happy V1.stl';


const url = svg;

const modelStyle = {
  width: '100vw',
  height: '75vh',
}

const modelProps={
  scale:1.5
}

function App() {
  return (
    <div className="App">
      <header className="App-header">    

        <h1>AI Audio Model Synthesiser</h1>
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          This is the STL model it takes an URI/URL as the source for an .stl.

        </p>

        <button onClick = {buttonOnClick}>
          Click Me!
        </button>

        <StlViewer
            id='STLViewer'
            style={modelStyle}
            scale={50}
            orbitControls
            shadows={true}
            url={url}
            modelProps={modelProps}
        />

      </header>
    </div>    
  );
}

function buttonOnClick(){
  alert("Button Clicked")
}

ReactDOM.render(<App/>,document.getElementById('root'));
export default App;