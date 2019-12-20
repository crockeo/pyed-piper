import React from "react";

import logo from "../res/logo.svg";
import "../styles/App.css";

import SynthButton from "./SynthButton";

const App: React.FC = () => {
  const synthButtons = [];
  for (let i = 0; i < 16; i++) {
    synthButtons.push(<SynthButton key={i} buttonIndex={i} />);
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a className="App-link" href="https://reactjs.org" target="_blank" rel="noopener noreferrer">
          Learn React
        </a>

        {synthButtons}
      </header>
    </div>
  );
};

export default App;
