import React from "react";

import pause from "../res/pause.svg";
import play from "../res/play.svg";
import "../styles/PlayButton.scss";

interface IPlayButtonProps {
  children?: React.ReactNode;
  onClick?: (event: React.MouseEvent<HTMLElement, MouseEvent>) => void | undefined;
  running: boolean;
}

const PlayButton: React.FC<IPlayButtonProps> = (props: IPlayButtonProps) => {
  return (
    <button className="PlayButton" onClick={props.onClick}>
      <img src={props.running ? pause : play} className="play" alt="play" />
    </button>
  );
};

export default PlayButton;
