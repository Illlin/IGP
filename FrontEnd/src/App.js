import React, {useState,} from 'react';
import ReactDOM from 'react-dom';
import {StlViewer} from "react-stl-viewer";
import urlHappy from './Datastore/Happy V1.stl';
import urlAngry from './Datastore/Angry V1.stl';
import AudioComponent from './AudioComponent';

function App() {
  return (
    <body className="App-body">    
      <div className="App">
        <header className='App-header'>
          <div>
            <h1>AI Audio Model Synthesiser</h1>
          </div>
        </header>
        <AudioComponent/>
        <ModelViewer></ModelViewer>
      </div>    
    </body>
  );
}

function urlSwitch(url){
  if (urlAngry===url){return urlHappy}
  else{return urlAngry}
}

function StlViewerComponent(props){ 
    const modelStyle = {
      width: '100vw',
      height: '75vh',
    };

    const modelProps={
      color:'#6929C4'
    };
    
    return (
        <StlViewer
          id='STLViewer'
          style={modelStyle}
          orbitControls
          shadows={true}
          url={props.url}
          modelProps={modelProps} />
    );
}

function ModelViewer() {
    const [url, setUrl] = useState(urlAngry);
    return (
      <div>
        <StlViewerComponent url={url}/>  
        <button onClick={() => setUrl(urlSwitch(url))} >Click to Change Model</ button>
        <button>
          <a href={url} download>Download .STL</a>
        </ button>
      </div>
    );
}

ReactDOM.render(<App/>,document.getElementById('root'));
export default App;