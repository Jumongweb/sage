# Quick Start - Sage Voice Assistant

## 🚀 5-Minute Setup

### Step 1: Install Dependencies (2 min)

```bash
# Activate virtual environment
source .venv/bin/activate

# Install packages
pip install -r requirements.txt

# If pyaudio fails:
brew install portaudio
pip install pyaudio
```

### Step 2: Test Installation (1 min)

```bash
python3 test_installation.py
```

### Step 3: Run Sage (2 min)

```bash
python3 main.py
```

Now say: **"Hey Siri"** (temporary placeholder for "Hey Sage")

Then give a command:
- "What time is it?"
- "Mute volume"
- "Open WhatsApp"

## 🎯 Current Status

✅ **Working now:**
- Wake word: "Hey Siri" (placeholder)
- All voice commands functional
- Volume control (mute, unmute, up, down)
- App control (WhatsApp, Notes)
- Social media shortcuts

⏳ **Optional next step:**
- Train custom "Hey Sage" wake word (see [TRAIN_WAKE_WORD.md](TRAIN_WAKE_WORD.md))
- Set up auto-start (see [SETUP_GUIDE.md](SETUP_GUIDE.md))

## 🔧 Common Issues

**Microphone not working?**
- System Preferences → Security & Privacy → Microphone
- Grant permission to Terminal/Python

**Wake word not detecting?**
- Speak clearly: "Hey Siri"
- Reduce background noise
- Check microphone is working

**Import errors?**
- Make sure you activated venv: `source .venv/bin/activate`
- Reinstall: `pip install -r requirements.txt`

## 📚 Full Documentation

- **[README.md](README.md)** - Overview and features
- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Detailed setup and auto-start
- **[TRAIN_WAKE_WORD.md](TRAIN_WAKE_WORD.md)** - Custom "Hey Sage" wake word

---

**That's it!** You're ready to use Sage. Say "Hey Siri" to activate! 🎉
