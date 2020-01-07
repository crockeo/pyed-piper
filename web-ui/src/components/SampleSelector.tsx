import React from "react";

import { IWavFile } from "../types";

interface ISampleSelectorProps {
  children?: React.ReactChildren;
  onSelect?: (wavfile: IWavFile) => any;
  value?: string;
  wavFiles: IWavFile[];
}

const SampleSelector: React.FC<ISampleSelectorProps> = (props: ISampleSelectorProps) => {
  return (
    <select className="sample-selector" value={props.value}>
      <option>Select a Sample</option>
      {props.wavFiles.map((wavFile, i) => (
        <option key={i} value={wavFile.id}>
          {wavFile.name}
        </option>
      ))}
    </select>
  );
};

export default SampleSelector;
