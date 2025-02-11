import argparse
import time
import threading
import pyaudio
import numpy as np
from pynput import keyboard

# from whisper import load_model

# added because of MLX
import mlx_whisper
from mlx_whisper.load_models import load_model

import platform


class SpeechTranscriber:

    def __init__(self, model_name, language=None, custom_vocabulary=None):
        self.model_name = model_name
        self.language = language
        self.custom_vocabulary = custom_vocabulary
        self.pykeyboard = keyboard.Controller()

    def transcribe(self, audio_data):
        result = mlx_whisper.transcribe(
            audio_data,
            path_or_hf_repo=self.model_name,
            language=self.language,
            initial_prompt=self.custom_vocabulary,
        )

        # MLX Whisper returns a dict with 'text' as a string
        text = result["text"].strip()

        # Split text into words and type them with spaces in between
        words = text.split()
        for i, word in enumerate(words):
            self.pykeyboard.type(word)
            # Add space between words, but not after the last word
            if i < len(words) - 1:
                self.pykeyboard.press(keyboard.Key.space)
                self.pykeyboard.release(keyboard.Key.space)


class Recorder:
    def __init__(self, transcriber):
        self.recording = False
        self.transcriber = transcriber

    def start(self):
        thread = threading.Thread(target=self._record_impl)
        thread.start()

    def stop(self):
        self.recording = False

    def _record_impl(self):
        self.recording = True
        frames_per_buffer = 1024
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            frames_per_buffer=frames_per_buffer,
            input=True,
        )
        frames = []

        while self.recording:
            data = stream.read(frames_per_buffer)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        audio_data = np.frombuffer(b"".join(frames), dtype=np.int16)
        audio_data_fp32 = audio_data.astype(np.float32) / 32768.0
        self.transcriber.transcribe(audio_data_fp32)


class GlobalKeyListener:
    def __init__(self, recorder, key_combination):
        self.recorder = recorder
        self.key1, self.key2 = self.parse_key_combination(key_combination)
        self.key1_pressed = False
        self.key2_pressed = False
        self.is_recording = False

    def parse_key_combination(self, key_combination):
        key1_name, key2_name = key_combination.split("+")
        key1 = getattr(keyboard.Key, key1_name, keyboard.KeyCode(char=key1_name))
        key2 = getattr(keyboard.Key, key2_name, keyboard.KeyCode(char=key2_name))
        return key1, key2

    def on_key_press(self, key):
        if key == self.key1:
            self.key1_pressed = True
        elif key == self.key2:
            self.key2_pressed = True

        if self.key1_pressed and self.key2_pressed:
            if not self.is_recording:
                print("Listening...")
                self.recorder.start()
                self.is_recording = True
            else:
                print("Transcribing...")
                self.recorder.stop()
                self.is_recording = False
                print("Done.")

    def on_key_release(self, key):
        if key == self.key1:
            self.key1_pressed = False
        elif key == self.key2:
            self.key2_pressed = False


def parse_args():
    parser = argparse.ArgumentParser(
        description="Dictation app using the MLX OpenAI Whisper model.",
    )
    parser.add_argument(
        "-m",
        "--model_name",
        type=str,
        choices=[
            "mlx-community/whisper-large-v3-mlx",
            "mlx-community/whisper-tiny-mlx-q4",
            "mlx-community/whisper-large-v2-mlx-fp32",
            "mlx-community/whisper-tiny.en-mlx-q4",
            "mlx-community/whisper-base.en-mlx-q4",
            "mlx-community/whisper-small.en-mlx-q4",
            "mlx-community/whisper-tiny-mlx-fp32",
            "mlx-community/whisper-base-mlx-fp32",
            "mlx-community/whisper-small-mlx-fp32",
            "mlx-community/whisper-medium-mlx-fp32",
            "mlx-community/whisper-base-mlx-2bit",
            "mlx-community/whisper-tiny-mlx-8bit",
            "mlx-community/whisper-tiny.en-mlx-4bit",
            "mlx-community/whisper-base-mlx",
            "mlx-community/whisper-base-mlx-8bit",
            "mlx-community/whisper-base.en-mlx-4bit",
            "mlx-community/whisper-small-mlx",
            "mlx-community/whisper-small-mlx-8bit",
            "mlx-community/whisper-small.en-mlx-4bit",
            "mlx-community/whisper-medium-mlx-8bit",
            "mlx-community/whisper-medium.en-mlx-8bit",
            "mlx-community/whisper-large-mlx-4bit",
            "mlx-community/whisper-large-v1-mlx",
            "mlx-community/whisper-large-v1-mlx-8bit",
            "mlx-community/whisper-large-v2-mlx-8bit",
            "mlx-community/whisper-large-v2-mlx-4bit",
            "mlx-community/whisper-large-v1-mlx-4bit",
            "mlx-community/whisper-large-mlx-8bit",
            "mlx-community/whisper-large-mlx",
            "mlx-community/whisper-medium.en-mlx-4bit",
            "mlx-community/whisper-small.en-mlx-8bit",
            "mlx-community/whisper-small.en-mlx",
            "mlx-community/whisper-small-mlx-4bit",
            "mlx-community/whisper-base.en-mlx-8bit",
            "mlx-community/whisper-base.en-mlx",
            "mlx-community/whisper-base-mlx-4bit",
            "mlx-community/whisper-tiny.en-mlx-8bit",
            "mlx-community/whisper-tiny.en-mlx",
            "mlx-community/whisper-tiny-mlx",
            "mlx-community/whisper-medium.en-mlx-fp32",
            "mlx-community/whisper-small.en-mlx-fp32",
            "mlx-community/whisper-base.en-mlx-fp32",
            "mlx-community/whisper-tiny.en-mlx-fp32",
            "mlx-community/whisper-medium-mlx-q4",
            "mlx-community/whisper-small-mlx-q4",
            "mlx-community/whisper-base-mlx-q4",
            "mlx-community/whisper-large-v3-turbo",
            "mlx-community/whisper-turbo",
        ],
        default="mlx-community/whisper-large-v3-mlx",
        help="Specify the MLX Whisper model to use.",
    )
    parser.add_argument(
        "-l",
        "--language",
        type=str,
        default=None,
        help='Specify the two-letter language code (e.g., "en" for English) to improve recognition accuracy. '
        "This can be especially helpful for smaller model sizes.  To see the full list of supported languages, "
        "check out the official list [here](https://github.com/openai/whisper/blob/main/whisper/tokenizer.py).",
    )
    parser.add_argument(
        "-t",
        "--max_time",
        type=float,
        default=30,
        help="Specify the maximum recording time in seconds. The app will automatically stop recording after this duration. "
        "Default: 30 seconds.",
    )
    parser.add_argument(
        "-k",
        "--key_combination",
        type=str,
        default="cmd_l+alt" if platform.system() == "Darwin" else "ctrl+alt",
        help="Specify the key combination to toggle recording. Example: cmd_l+alt for macOS "
        "or ctrl+alt for other platforms.",
    )
    parser.add_argument(
        "-cv",
        "--custom_vocabulary",
        type=str,
        default="",
        help="Specify a comma separated list of custom vocabulary to improve recognition accuracy.",
    )

    args = parser.parse_args()

    if args.model_name.endswith(".en") and args.language != "en":
        raise ValueError(
            "If using a model ending in .en, you cannot specify a language other than English."
        )

    return args


if __name__ == "__main__":
    args = parse_args()

    model_name = args.model_name
    transcriber = SpeechTranscriber(
        model_name, custom_vocabulary=args.custom_vocabulary
    )
    recorder = Recorder(transcriber)

    # Create and start the key listener
    key_listener = GlobalKeyListener(recorder, args.key_combination)
    listener = keyboard.Listener(
        on_press=key_listener.on_key_press, on_release=key_listener.on_key_release
    )
    listener.start()

    print(f"Ready. Press {args.key_combination} to start/stop recording...")

    # Keep the main thread running
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nExiting...")
