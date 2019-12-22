import React from "react";

import logo from "../res/logo.svg";
import "../styles/App.scss";

const App: React.FC = () => {
  return (
    <div className="App">
      <div className="header">
        <img src={logo} className="logo" alt="logo" />
        <span className="title">Pyed Piper</span>
      </div>

      <div className="body">TODO</div>
    </div>
  );
};

export default App;
