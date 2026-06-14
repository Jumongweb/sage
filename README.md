# Sage - Personal Voice Assistant

A local voice-activated assistant with wake word detection.

## Features

- 🎙️ **Wake Word Detection** - Say "Hey Sage" to activate
- 🗣️ **Voice Commands** - Control your Mac with voice
- 🔊 **Volume Control** - Mute, unmute, increase, decrease volume
- 📱 **App Control** - Open/close WhatsApp, Notes, and more
- 🌐 **Social Media** - Quick access to Facebook, Instagram, Twitter, etc.
- 📅 **Schedule** - Check your daily schedule
- ⏰ **Time & Date** - Ask for current time

## Quick Start

### 1. Install Dependencies

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

If `pyaudio` fails to install:
```bash
brew install portaudio
pip install pyaudio
```

### 2. Run Sage

```bash
python3 main.py
```

### 3. Set Up Auto-Start (Optional)

To make Sage start automatically when you log in:

```bash
./install_autostart.sh
```

To remove auto-start:
```bash
./uninstall_autostart.sh
```

## Usage

1. Say **"Hey Sage"** (wake word)
   - **Note:** Currently using "Hey Siri" as placeholder. See [TRAIN_WAKE_WORD.md](TRAIN_WAKE_WORD.md) to train custom "Hey Sage"
2. Wait for "Yes, Codefather?"
3. Give your command:
   - "What time is it?"
   - "Open WhatsApp"
   - "Mute volume"
   - "Volume up"
   - "Check my schedule"
   - "Open Facebook"
   - And many more!

## Available Commands

- **Time & Greetings**: "hello", "what time is it"
- **Volume Control**: "volume up", "volume down", "mute", "unmute"
- **Apps**: "open WhatsApp", "close WhatsApp", "open notes", "close notes"
- **Social Media**: "open facebook/instagram/twitter/linkedin/github"
- **Schedule**: "check my schedule"
- **Exit**: "exit", "quit", "stop"

## File Structure

- `main.py` - Main application
- `launch_sage.sh` - Launch script
- `requirements.txt` - Python dependencies
- `install_autostart.sh` - Auto-start installer
- `uninstall_autostart.sh` - Auto-start remover
- `SETUP_GUIDE.md` - Detailed setup instructions

## Customization

See `SETUP_GUIDE.md` for:
- Changing the wake word
- Customizing voice settings
- Adding new commands

See `TRAIN_WAKE_WORD.md` for:
- Training custom "Hey Sage" wake word
- Platform-specific setup
- Wake word troubleshooting

## Troubleshooting

Check `SETUP_GUIDE.md` for detailed troubleshooting steps.

Quick checks:
- Microphone permissions in System Preferences
- Check logs: `tail -f logs/sage.log`
- Verify service: `launchctl list | grep sage`

## Credits

Built with:
- Porcupine (wake word detection)
- pyttsx3 (text-to-speech)
- SpeechRecognition (speech-to-text)

---

For detailed setup and configuration, see [SETUP_GUIDE.md](SETUP_GUIDE.md)
