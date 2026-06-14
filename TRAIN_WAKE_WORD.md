# Training Custom "Hey Sage" Wake Word

The app currently uses "Hey Siri" as a placeholder wake word. To use the actual "Hey Sage" wake word, you need to train a custom model.

## Step-by-Step Guide

### 1. Create Picovoice Account

1. Go to [https://console.picovoice.ai/](https://console.picovoice.ai/)
2. Sign up for a free account (personal use is free)
3. Verify your email

### 2. Train "Hey Sage" Wake Word

1. Log in to Picovoice Console
2. Click on **"Porcupine"** (Wake Word)
3. Click **"Train Wake Word"** or **"Create New"**
4. Enter the wake word phrase: **"Hey Sage"**
5. Select the platform: **Mac (x86_64)** or **Mac (arm64)** depending on your Mac
   - Apple Silicon (M1/M2/M3): Choose **arm64**
   - Intel Mac: Choose **x86_64**
6. Click **"Train"**
7. Wait for training to complete (usually a few minutes)
8. Download the `.ppn` file

### 3. Add the Wake Word File to Your Project

1. Save the downloaded file as `hey_sage.ppn` in your project directory:
   ```bash
   mv ~/Downloads/Hey-Sage_en_mac_v3_0_0.ppn /Users/macbook/Projects/jarvis/hey_sage.ppn
   ```

### 4. Update the Code

Open `main.py` and find the `wait_for_wake_word()` function. Change this line:

```python
# Old (placeholder):
porcupine = pvporcupine.create(keywords=['hey siri'])

# New (custom wake word):
porcupine = pvporcupine.create(keyword_paths=['/Users/macbook/Projects/jarvis/hey_sage.ppn'])
```

### 5. Test It

```bash
python3 main.py
```

Now say "Hey Sage" and it should detect your custom wake word!

## Alternative: Use Built-in Wake Words for Testing

If you don't want to train a custom wake word yet, you can use any of these built-in options:

```python
# In wait_for_wake_word() function:
porcupine = pvporcupine.create(keywords=['hey siri'])    # Current
porcupine = pvporcupine.create(keywords=['alexa'])
porcupine = pvporcupine.create(keywords=['computer'])
porcupine = pvporcupine.create(keywords=['hey google'])
porcupine = pvporcupine.create(keywords=['jarvis'])
porcupine = pvporcupine.create(keywords=['picovoice'])
```

## Troubleshooting

### "Invalid keyword_paths" Error
- Make sure the path to your `.ppn` file is correct
- Use absolute path: `/Users/macbook/Projects/jarvis/hey_sage.ppn`

### Wake Word Not Detecting
- Make sure you trained for the correct platform (arm64 vs x86_64)
- Check your microphone is working
- Try saying the wake word more clearly
- Reduce background noise

### Platform Mismatch
If you get a platform error, check your Mac type:
```bash
uname -m
# arm64 = Apple Silicon (M1/M2/M3)
# x86_64 = Intel Mac
```

Then train the wake word for the correct platform.

## Free Tier Limits

Picovoice free tier (for personal use) includes:
- Unlimited wake word training
- Up to 3 custom wake words
- Commercial use requires paid license

For more info: [https://picovoice.ai/pricing/](https://picovoice.ai/pricing/)
