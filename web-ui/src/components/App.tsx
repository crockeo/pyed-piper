import axios from "axios";
import React from "react";

import logo from "../res/logo.svg";
import "../styles/App.scss";

import AddSample from "./AddSample";
import SynthButton from "./SynthButton";

import { SERVER_URI, GET_BUTTONS_URI, GET_SAMPLES_URI } from "../consts";
import { IWavFile, ISynthButtonSetting } from "../types";

interface IAppProps {
  children?: React.ReactChildren;
}

interface IAppState {
  error: string | null;
  mode: "loading" | "ready" | "failed";
  synthButtonSettings: Array<ISynthButtonSetting>;
  wavFiles: Array<IWavFile>;
}

class App extends React.Component<IAppProps, IAppState> {
  constructor(props: IAppProps) {
    super(props);

    this.state = {
      error: null,
      mode: "loading",
      synthButtonSettings: [],
      wavFiles: []
    };
  }

  componentDidMount() {
    Promise.all([axios.get(SERVER_URI + GET_BUTTONS_URI), axios.get(SERVER_URI + GET_SAMPLES_URI)])
      .then(res => {
        this.setState({
          synthButtonSettings: res[0].data,
          wavFiles: res[1].data
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

        <div className="body">
          <div className="button-grid">
            {this.state.synthButtonSettings.map((synthButtonSetting, i) => (
              <SynthButton setting={synthButtonSetting} wavFiles={this.state.wavFiles} key={i} />
            ))}
          </div>

          <div className="add-sample-container">
            <AddSample />
          </div>
        </div>
      </div>
    );
  }
}

export default App;
