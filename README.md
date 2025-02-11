# Multilingual Dictation Script based on OpenAI Whisper

Want to use real-time dictation on your Mac but don't want to pay a monthly fee for one of those new fancy dictation apps?
This script is for you!

It is a multilingual dictation script based on the powerful OpenAI Whisper ASR model(s) to provide accurate and efficient speech-to-text conversion in any application. The script runs in the background and is triggered through a keyboard shortcut. It is also entirely offline, so no data will be shared. It allows users to set up their own keyboard combinations and choose from different Whisper models, and languages.

## Prerequisites

The PortAudio and llvm library is required for this app to work. You can install it on macOS using the following command:

```bash
brew install portaudio llvm
```

## Permissions

The app requires accessibility permissions to register global hotkeys and permission to access your microphone for speech recognition.

## Installation

Clone the repository:

```bash
git clone https://github.com/foges/whisper-dictation.git
cd whisper-dictation
```

If you use poetry:

```shell
poetry install
poetry shell
```

Or, if you don't use poetry, first create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the application:

```bash
python whisper-dictation.py
```

By default, the app uses the "base" Whisper ASR model and the key combination to toggle dictation is cmd+option on macOS and ctrl+alt on other platforms. You can change the model and the key combination using command-line arguments. For best results on modern Macs with M-series chips, I recommend using the large-v3-turbo model which provides excellent accuracy while maintaining good performance. For example:

```bash
python whisper-dictation.py -m mlx-community/whisper-large-v3-turbo
```

The models are multilingual, and you can specify a two-letter language code (e.g., "no" for Norwegian) with the `-l` or `--language` option. Specifying the language can improve recognition accuracy, especially for smaller model sizes.
