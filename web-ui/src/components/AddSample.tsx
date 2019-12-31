import axios from "axios";
import React from "react";

import { SERVER_URI, POST_SAMPLE_URI } from "../consts";
import "../styles/AddSample.scss";

interface IAddSampleProps {
  children?: React.ReactNode;
}

class AddSample extends React.PureComponent<IAddSampleProps> {
  fileInput: React.RefObject<HTMLInputElement>;

  constructor(props: IAddSampleProps) {
    super(props);
    this.fileInput = React.createRef();
  }

  postWav: React.FormEventHandler<HTMLFormElement> = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    const file = this.fileInput.current?.files?.item(0);
    if (!file) {
      // TODO: better handle error
      return;
    }

    if (file.type !== "audio/wav") {
      // TODO: better handle error
      return;
    }

    const formData = new FormData();
    formData.append("sampleFile", file);

    axios
      .post(SERVER_URI + POST_SAMPLE_URI, formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        }
      })
      .then(res => {
        console.log(res);
      })
      .catch(err => {
        console.log(err);
      });
  };

  render() {
    return (
      <form className="add-sample" onSubmit={this.postWav}>
        <div className="add-sample-title">Add a New Sample</div>

        <div>
          <input className="add-sample-file" type="file" ref={this.fileInput} />
        </div>

        <div>
          <input className="add-sample-submit" type="submit" />
        </div>
      </form>
    );
  }
}

export default AddSample;
