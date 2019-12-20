import React from "react";

interface ISynthButtonProps {
  buttonIndex: number;
  children?: React.ReactNode;
}

interface ISynthButtonState {}

class SynthButton extends React.Component<ISynthButtonProps, ISynthButtonState> {
  render() {
    return <div>Hello {this.props.buttonIndex}</div>;
  }
}

export default SynthButton;
