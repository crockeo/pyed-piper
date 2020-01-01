import React from "react";

interface ISynthButtonSetting {
  mode: "tone" | "wav";
}

interface ISynthButtonProps {
  children?: React.ReactChildren;
  setting: ISynthButtonSetting;
}

class SynthButton extends React.Component<ISynthButtonProps> {
  render() {
    return <div>Hell world</div>;
  }
}
