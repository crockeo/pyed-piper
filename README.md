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

TODO

### HTTP API

TODO

## Web UI

TODO

### Installation

TODO

### Usage

TODO

## License

MIT Open Source License. Refer to the `LICENSE` file for information.
