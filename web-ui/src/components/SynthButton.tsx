import _ from "lodash";
import React, { ChangeEvent } from "react";

import "../styles/SynthButton.scss";

import SampleSelector from "./SampleSelector";

import { ISynthButtonSetting, IWavFile } from "../types";

interface ISynthButtonProps {
  children?: React.ReactChildren;
  onSettingUpdate: (setting: ISynthButtonSetting) => any;
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

  componentDidUpdate() {
    // Whenever we receive an update from outside, override internal changes.
    // Used to sync with the server, once we receive a reply from a PUT.
    if (this.props.setting !== this.state.localSetting) {
      this.setState({
        localSetting: this.props.setting
      });
    }
  }

  // Used whenever we want to update the SynthButtonSetting that exists in the
  // server.
  _debouncedOnSettingUpdate = _.debounce(this.props.onSettingUpdate, 500);

  _setLocalSettingField(field: keyof ISynthButtonSetting) {
    return (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
      event.persist();

      let value: string | number = event.target.value;
      if (typeof this.state.localSetting[field] === "number") {
        value = Number.parseFloat(value);
      }

      if (value === this.state.localSetting[field]) {
        return;
      }

      this.setState(
        prevState => _.set(prevState, ["localSetting", field], value),
        () => {
          if (this._isValidUpdate(field, value)) {
            this._debouncedOnSettingUpdate(this.state.localSetting);
          } else {
            this._debouncedOnSettingUpdate.cancel();
          }
        }
      );
    };
  }

  _isValidUpdate(field: keyof ISynthButtonSetting, value: string | number): boolean {
    return !(field === "mode" || value === 0 || value === "" || (typeof value === "number" && isNaN(value)));
  }

  _renderNumber(n: number): string {
    if (isNaN(n)) {
      return "";
    }

    return n.toString();
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
        <select onChange={this._setLocalSettingField("mode")} value={this.state.localSetting.mode}>
          <option value="tone">Tone</option>
          <option value="wav">Wav</option>
        </select>

        <div>
          <label>Linger Time</label>
          <input
            type="number"
            placeholder="Linger Time"
            min="0.001"
            onChange={this._setLocalSettingField("linger_time")}
            value={this._renderNumber(this.state.localSetting.linger_time)}
          />
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
        <input
          type="number"
          placeholder="Frequency"
          min="0"
          onChange={this._setLocalSettingField("frequency")}
          value={this._renderNumber(this.state.localSetting.frequency || NaN)}
        />

        <label>Overtones</label>
        <input
          type="number"
          placeholder="Overtones"
          min="1"
          onChange={this._setLocalSettingField("overtones")}
          value={this._renderNumber(this.state.localSetting.overtones || NaN)}
        />
      </div>
    );
  }

  renderWavConfig() {
    return (
      <div className="config-section">
        <div className="config-header">Wav Config</div>

        <SampleSelector
          onChange={this._setLocalSettingField("wav_id")}
          value={this.state.localSetting.wav_id || undefined}
          wavFiles={this.props.wavFiles}
        />
      </div>
    );
  }
}

export default SynthButton;
