begin new tentative instructions

Enter /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)" in terminal to download home-brew

Enter export PATH="/opt/homebrew/bin:$PATH" in terminal to add home-brew to ur path

nano ~/.zshrc

Paste source ~/.zshrc

Ctrl x, y, enter

Paste source ~/.zshrc


Enter brew install portaudio llvm in terminal to download these required packages for the app

In ur documents folder: Git clone https://github.com/computerstimulation/mlx-whisper-dictation

Cd mlx whisper dictation

Create a virtual environment: 
python3.11 -m venv venv              
source venv/bin/activate

Install the rest of the app’s required packages
pip install -r requirements.txt

Wait for dependencies to download

Run the app using this command: 
python whisper-dictation.py

Go to a text field have ur cursor on it

Press command option

If prompted with “Terminal” would like to access the microphone. Press Allow

Speak

Press command option

Wait for model to download if first time using app

Default model is mlx whisper large (highest quality, slowest time)

You can change the model

If your cursor is still on your text field you may see the text being automatically pasted

Press control c in terminal to turn off the app

end new tentative instructions

# Multilingual Dictation App based on OpenAI Whisper
Multilingual dictation app based on the open-source Apple MLX (does not seem to be an abbreviation officially, although one might infer that it stands for Machine Learning "X", with "X" being whatever your mind wants it to be) OpenAI Whisper speech-to-text model(s) to provide accurate and efficient speech-to-text conversion in any application. The app runs in the background and is triggered through a keyboard shortcut. It allows users to set up their own keyboard combinations and choose from different MLX Whisper models, and languages.

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

By default, the app uses the "base" Whisper ASR model and the key combination to toggle dictation is cmd+option on macOS and ctrl+alt on other platforms. You can change the model and the key combination using command-line arguments.  Note that models other than `tiny` and `base` can be slow to transcribe and are not recommended unless you're using a powerful computer, ideally one with a CUDA-enabled GPU. For example:


```bash
python whisper-dictation.py -m large -k cmd_r+shift -l en
```

The models are multilingual, and you can specify a two-letter language code (e.g., "no" for Norwegian) with the `-l` or `--language` option. Specifying the language can improve recognition accuracy, especially for smaller model sizes.

#### Replace macOS default dictation trigger key
You can use this app to replace macOS built-in dictation. Trigger to begin recording with a double click of Right Command key and stop recording with a single click of Right Command key.
```bash
python whisper-dictation.py -m large --k_double_cmd -l en
```
To use this trigger, go to System Settings -> Keyboard, disable Dictation. If you double click Right Command key on any text field, macOS will ask whether you want to enable Dictation, so select Don't Ask Again.

## Setting the App as a Startup Item
To have the app run automatically when your computer starts, follow these steps:

 1. Open System Preferences.
 2. Go to Users & Groups.
 3. Click on your username, then select the Login Items tab.
 4. Click the + button and add the `run.sh` script from the whisper-dictation folder.

# Installation and Usage Instructions for MLX Whisper Dictation

## Step 1: Install Homebrew
Run the following command in your terminal to install Homebrew:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
Add Homebrew to your path:

bash
Copy code
export PATH="/opt/homebrew/bin:$PATH"
Step 2: Configure Zsh
Open your Zsh configuration file:

bash
Copy code
nano ~/.zshrc
Add the following line to the file:

bash
Copy code
source ~/.zshrc
Save and exit the file:

Press Ctrl + X
Press Y
Press Enter
Then reload the Zsh configuration:

bash
Copy code
source ~/.zshrc
Step 3: Install Required Packages
Run the following command to install required packages:

bash
Copy code
brew install portaudio llvm
Step 4: Clone the Repository
Navigate to your Documents folder and clone the repository:

bash
Copy code
cd ~/Documents
git clone https://github.com/computerstimulation/mlx-whisper-dictation
Navigate into the project directory:

bash
Copy code
cd mlx-whisper-dictation
Step 5: Set Up a Virtual Environment
Create and activate a virtual environment:

bash
Copy code
python3.11 -m venv venv
source venv/bin/activate
Step 6: Install Dependencies
Install the required packages for the app:

bash
Copy code
pip install -r requirements.txt
Wait for the dependencies to download.

Step 7: Run the App
Run the application using:

bash
Copy code
python whisper-dictation.py
Step 8: Use the App
Open a text field and place your cursor on it.
Press Command + Option.
If prompted with “Terminal would like to access the microphone,” press Allow.
Start speaking into your microphone.
Press Command + Option again to stop.