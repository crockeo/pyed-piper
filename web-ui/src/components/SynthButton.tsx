import React from "react";

import pause from "../res/pause.svg";
import play from "../res/play.svg";
import "../styles/SynthButton.scss";

interface ISynthButtonProps {
  children?: React.ReactNode;
  onClick?: (event: React.MouseEvent<HTMLElement, MouseEvent>) => void | undefined;
  running: boolean;
}

const SynthButton: React.FC<ISynthButtonProps> = (props: ISynthButtonProps) => {
  return (
    <button className="SynthButton" onClick={props.onClick}>
      <img src={props.running ? pause : play} className="play" alt="play" />
    </button>
  );
};

export default SynthButton;
