import React from "react";

import logo from "../res/logo.svg";
import "../styles/App.scss";

import AddSample from "./AddSample";
import SynthButton from "./SynthButton";

const App: React.FC = () => {
  return (
    <div className="App">
      <div className="header">
        <img src={logo} className="logo" alt="logo" />
        <span className="title">Pyed Piper</span>
      </div>

      <AddSample />

      <div className="body">
        <div className="button-grid">
          {new Array(16).fill(0).map((_, i) => (
            <SynthButton running={i % 2 === 0} key={i} />
          ))}
        </div>
      </div>
    </div>
  );
};

export default App;
