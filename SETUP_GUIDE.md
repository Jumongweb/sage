# Sage Setup Guide

## 1. Install Dependencies

First, install the required Python packages:

```bash
# Activate your virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

**Note:** If you encounter issues installing `pyaudio`, you may need to install portaudio first:

```bash
brew install portaudio
pip install pyaudio
```

## 2. Test the Application

Run the application manually to ensure everything works:

```bash
python3 main.py
```

You should now be able to:
1. Say "Hey Sage" as the wake word
2. Wait for the response "Yes, Codefather?"
3. Give your command (e.g., "what time is it", "open WhatsApp", "mute volume")

## 3. Auto-Start on macOS Login

### Option A: Using LaunchAgent (Recommended)

Create a LaunchAgent plist file:

```bash
mkdir -p ~/Library/LaunchAgents
```

Create the file `~/Library/LaunchAgents/com.sage.assistant.plist` with the following content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.sage.assistant</string>
    
    <key>ProgramArguments</key>
    <array>
        <string>/Users/macbook/Projects/jarvis/launch_sage.sh</string>
    </array>
    
    <key>RunAtLoad</key>
    <true/>
    
    <key>KeepAlive</key>
    <true/>
    
    <key>StandardOutPath</key>
    <string>/Users/macbook/Projects/jarvis/logs/sage.log</string>
    
    <key>StandardErrorPath</key>
    <string>/Users/macbook/Projects/jarvis/logs/sage_error.log</string>
    
    <key>WorkingDirectory</key>
    <string>/Users/macbook/Projects/jarvis</string>
</dict>
</plist>
```

Create the logs directory:

```bash
mkdir -p /Users/macbook/Projects/jarvis/logs
```

Load the LaunchAgent:

```bash
launchctl load ~/Library/LaunchAgents/com.sage.assistant.plist
```

To start it immediately:

```bash
launchctl start com.sage.assistant
```

**Useful Commands:**

```bash
# Check if it's running
launchctl list | grep sage

# Stop the service
launchctl stop com.sage.assistant

# Unload (disable auto-start)
launchctl unload ~/Library/LaunchAgents/com.sage.assistant.plist

# Reload after making changes
launchctl unload ~/Library/LaunchAgents/com.sage.assistant.plist
launchctl load ~/Library/LaunchAgents/com.sage.assistant.plist
```

### Option B: Using Login Items (Simple GUI Method)

1. Open **System Preferences** → **Users & Groups** (or **General** → **Login Items** on newer macOS)
2. Click on **Login Items** tab
3. Click the **+** button
4. Navigate to `/Users/macbook/Projects/jarvis/` and select `launch_sage.sh`
5. The app will now start automatically when you log in

**Note:** This method is simpler but doesn't keep the app alive if it crashes.

## 4. Troubleshooting

### Microphone Permission Issues

If the app can't access the microphone:

1. Go to **System Preferences** → **Security & Privacy** → **Microphone**
2. Grant permission to Terminal or Python
3. Restart the application

### Wake Word Not Working

- Make sure your microphone is working
- Check if background noise is too loud
- Try saying "Hey Sage" more clearly (currently using "Hey Siri" as placeholder)
- For true "Hey Sage" wake word, see customization section below
- Check the logs at `/Users/macbook/Projects/jarvis/logs/sage_error.log`

### App Not Starting at Login

- Check if the LaunchAgent is loaded: `launchctl list | grep sage`
- Check the error log: `cat ~/Projects/jarvis/logs/sage_error.log`
- Ensure the virtual environment path in `launch_sage.sh` is correct

## 5. Customization

### Change or Train Custom "Hey Sage" Wake Word

Currently, the app uses the built-in "Hey Siri" wake word as a placeholder. To use a true "Hey Sage" wake word:

1. Visit https://console.picovoice.ai/ (free for personal use)
2. Create an account
3. Go to "Wake Word" section
4. Train "Hey Sage" as your custom wake word
5. Download the `.ppn` file
6. Update `main.py`:

```python
# Replace this line in wait_for_wake_word():
porcupine = pvporcupine.create(keywords=['hey siri'])

# With:
porcupine = pvporcupine.create(keyword_paths=['/Users/macbook/Projects/jarvis/hey_sage.ppn'])
```

Available built-in wake words you can use temporarily:
- `'hey siri'` (current placeholder)
- `'alexa'`
- `'computer'`
- `'hey google'`
- `'jarvis'`
- `'picovoice'`
- `'porcupine'`
- `'terminator'`

## 6. Uninstall

To remove the auto-start:

```bash
# Stop and unload the service
launchctl stop com.sage.assistant
launchctl unload ~/Library/LaunchAgents/com.sage.assistant.plist

# Remove the plist file
rm ~/Library/LaunchAgents/com.sage.assistant.plist
```

---

## Quick Start Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Test manually
python3 main.py

# Set up auto-start (copy the plist content first)
mkdir -p ~/Library/LaunchAgents
# Create the plist file (see above)
launchctl load ~/Library/LaunchAgents/com.sage.assistant.plist
```

Now Sage will be ready to assist you whenever you say "Hey Sage"! 🎉
