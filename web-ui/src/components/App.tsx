import axios from "axios";
import React from "react";

import logo from "../res/logo.svg";
import "../styles/App.scss";

import AddSample from "./AddSample";
import PlayButton from "./PlayButton";

import { SERVER_URI, GET_SAMPLES_URI } from "../consts";
import { IWavFile } from "../types";

interface IAppProps {
  children?: React.ReactChildren;
}

interface IAppState {
  error: string | null;
  mode: "loading" | "ready" | "failed";
  wavFiles: Array<IWavFile>;
}

class App extends React.Component<IAppProps, IAppState> {
  constructor(props: IAppProps) {
    super(props);

    this.state = {
      error: null,
      mode: "loading",
      wavFiles: []
    };
  }

  componentDidMount() {
    axios
      .get(SERVER_URI + GET_SAMPLES_URI)
      .then(res => {
        this.setState({
          mode: "ready",
          wavFiles: res.data
        });
      })
      .catch(err => {
        this.setState({
          error: err.toString(),
          mode: "failed"
        });
      });
  }

  render() {
    return (
      <div className="App">
        <div className="header">
          <img src={logo} className="logo" alt="logo" />
          <span className="title">Pyed Piper</span>
        </div>

        <AddSample />

        <select>
          {this.state.wavFiles.map((wavFile, i) => (
            <option key={i} value={wavFile.id}>
              {wavFile.name}
            </option>
          ))}
        </select>

        <div className="body">
          <div className="button-grid">
            {new Array(16).fill(0).map((_, i) => (
              <div className="button-grid-entry" key={i}>
                <PlayButton running={i % 2 === 0} />
              </div>
            ))}
          </div>
        </div>
      </div>
    );
  }
}

export default App;
