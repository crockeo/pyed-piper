# pyed-piper

Web-configurable music synthesis for the Bongo (Crockeo?) Box.

## Server

This is the Python server part of the project. It handles music synthesis, and contains an HTTP API used to configure the synth. This HTTP API is used by the web UI, explained below.

### Installation

The server depends on native libraries, and so requires some setup beyond that of a normal Python library. This section assumes you're running macOS, but the process should be mostly the same across platforms.

#### On A Computer

First, ensure that you have Python 3 installed. To check if it is, run:

```bash
# If this says Python 3.x.x, you're fine!
$ python --version

# If it says Python 2.7.x, try:
$ python3 --version
```

If Python 3 is not installed, you can find it [here](https://www.python.org/downloads/). After installation, try again from the command line to make sure that you can run Python 3. Rembmer if you used `python` or `python3`. It will be relevant for which `pip`, the Python package manager, you want to use.

Next, you want to make sure that you have PortAudio installed. We use a library called PyAudio that depends PortAudio. For now, I will only cover installation for macOS. First, make sure you have brew installed.

```bash
$ brew --version
```

If you don't have it installed, refer to the [brew website](https://brew.sh/) for installation instructions. After it's installed, install PortAudio with Brew.

```bash
$ brew install portaudio
```

Now that PortAudio is installed, you can install the Python packages required to run the project.

```bash
# If you used python
$ pip install -r requirements.txt

# If you used python3
$ pip3 install -r requirements.txt
```

Now, you can run the synth by starting `main.py`. Note that the `keyboard` package, upon which it depends, needs root, so you'll need to `sudo` run it:

```bash
# If you used python
$ sudo python main.py

# If you used python3
$ sudo python3 main.py
```

#### On the Raspberry Pi

**TODO:** We have not begun setting up our Raspberry Pis, so this part is to come!

### Music Synthesis

Press buttons! On a QWERTY keyboard, bound to 1-8, and q-i. Wooh

### HTTP API

#### Buttons

- `GET`: `/button/count`

  Arguments: None

  Returns: `int`, count of buttons on the synth. Hard coded to `16` for now.

- `GET`: `/buttons`

  Arguments: None

  Returns: `Array` of `SynthButtonSetting`s, each in the form:

  ```json
  {
    "index": "int",
    "mode": "string ('tone' or 'wav')",
    "linger_time": "float",

    "frequency": "float",
    "overtones": "int",

    "wav_id": "string"
  }
  ```

- `GET`: `/button/<int:index>`

  Arguments: `int` index

  Returns: A single `SynthButtonSetting`, as described above.

- `PUT`: `/button/<int:index>`

  Arguments: Single `SynthButtonSetting`, in the form above, as the body of the message.

  Returns: The same `SynthButtonSetting` as processed by the server.

#### Samples

- `GET`: `/samples`

  Arguments: none

  Returns: An `Array` of `WavFile`s, in the form:

  ```json
  {
    "id": "string",
    "path": "string",
    "name": "string"
  }
  ```

- `GET`: `/sample/id`

  Arguments: `str` id

  Returns: A single `WavFile`, as described above.

- `POST`: `/sample`

  Arguments: A blob of type `audio/wav`

  Returns: A single `WavFile`, corresponding to the entry made in the database associated with the blob data.

## Web UI

This is a Node.js part of the project, meant to be hosted on the Raspberry Pi to configure the synth by connecting to the Pi in Access Point mode. You can also use it to configure the synth on the computer!

### Installation / Usage

All of the following commands assume that you're in the `web-ui` directory. Ensure that you have [Node.js](https://nodejs.org/en/) and [NPM](https://www.npmjs.com/) installed.

```bash
$ npm install
$ npm start
```

If you want to package the project to be served by another web server... then DIY until I get to that part of the project.

## License

MIT Open Source License. Refer to the `LICENSE` file for information.
