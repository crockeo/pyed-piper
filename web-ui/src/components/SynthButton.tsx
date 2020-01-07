import React from "react";

import "../styles/SynthButton.scss";

import SampleSelector from "./SampleSelector";

import { ISynthButtonSetting, IWavFile } from "../types";

interface ISynthButtonProps {
  children?: React.ReactChildren;
  setting: ISynthButtonSetting;
  wavFiles: IWavFile[];
}

interface ISynthButtonState {
  localSetting: ISynthButtonSetting;
}

class SynthButton extends React.Component<ISynthButtonProps, ISynthButtonState> {
  constructor(props: ISynthButtonProps) {
    super(props);

    this.state = {
      localSetting: props.setting
    };
  }

  _setMode(mode: string) {
    if (mode !== "tone" && mode !== "wav") {
      throw new Error(`Invalid mode "${mode}"`);
    }

    this.setState(prevState => ({
      localSetting: {
        ...prevState.localSetting,
        mode: mode
      }
    }));
  }

  getMode() {
    if (this.state.localSetting.mode === "tone") {
      return this.renderToneConfig();
    } else if (this.state.localSetting.mode === "wav") {
      return this.renderWavConfig();
    } else {
      throw new Error(`Encountered unexpected SynthButtonSetting ${this.props.setting.mode}`);
    }
  }

  render() {
    return (
      <div className="synth-button">
        <div className="synth-button-name">Button {this.state.localSetting.index}</div>
        <select onChange={evt => this._setMode(evt.target.value)} value={this.state.localSetting.mode}>
          <option value="tone">Tone</option>
          <option value="wav">Wav</option>
        </select>

        <div>
          <label>Linger Time</label>
          <input type="number" placeholder="Linger Time" value={this.state.localSetting.linger_time} />
        </div>

        {this.getMode()}
      </div>
    );
  }

  renderToneConfig() {
    return (
      <div className="config-section">
        <div className="config-header">Tone Config</div>

        <label>Frequency</label>
        <input type="number" placeholder="Frequency" value={this.state.localSetting.frequency || undefined} />

        <label>Overtones</label>
        <input type="number" placeholder="Overtones" value={this.state.localSetting.overtones || undefined} />
      </div>
    );
  }

  renderWavConfig() {
    return (
      <div className="config-section">
        <div className="config-header">Wav Config</div>

        <SampleSelector value={this.state.localSetting.wav_id || undefined} wavFiles={this.props.wavFiles} />
      </div>
    );
  }
}

export default SynthButton;
