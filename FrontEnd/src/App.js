import React, {useState} from 'react';
import ReactDOM from 'react-dom';
import AudioComponent from './Components/AudioComponents/AudioComponent';
import { ModelViewComponent } from '././Components/ModelComponents/ModelViewComponent';
import placeHolderStl from './Datastore/WaitingForModel.stl'

function App() {
  const [activeView, setActiveView] = useState(1);
  const [stlFile, setSTLFile] = useState(placeHolderStl);
  const handleCallbackViewSwitch = (stlData) =>{
    console.log("App.js handelcallback switch callled");
    viewSwitch(stlData);
  }
  const handelCallbackSetSTL = (stlURI) => {
    setSTLFile(stlURI);
  }    
  
  return (
    <body className="App-body">    
      <div className="App">
        <header className='App-header'></header>
        
        <AudioComponent 
          id="AudioComp"
          viewCallback={handleCallbackViewSwitch} 
          modelCallback={handelCallbackSetSTL} 
          render={activeView}
        />

        <ModelViewComponent viewCallback={handleCallbackViewSwitch} url={stlFile} render={activeView}/>

      </div>    
    </body>
  );






function viewSwitch(){
  if (activeView===1){
    setActiveView(0);
  }
  
  else{
    setActiveView(1)
  }
}


}
ReactDOM.render(<App/>,document.getElementById('root'));
export default App;