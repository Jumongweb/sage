# Getting Your Picovoice Access Key

Porcupine wake word detection requires a free access key from Picovoice.

## Quick Steps (2 minutes)

### 1. Create Free Account

Visit: **https://console.picovoice.ai/signup**

- Sign up with your email
- Verify your email address
- Log in to the console

### 2. Get Your Access Key

1. Once logged in, you'll see your dashboard
2. Look for **"AccessKey"** section (usually visible on the main page)
3. Copy your access key (it looks like: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxx==`)

### 3. Add Access Key to Sage

Create a file named `.env` in your project directory:

```bash
cd /Users/macbook/Projects/jarvis
touch .env
```

Open `.env` and add your access key:

```
PICOVOICE_ACCESS_KEY=your_access_key_here
```

Replace `your_access_key_here` with the actual key you copied.

**Example:**
```
PICOVOICE_ACCESS_KEY=abcd1234efgh5678ijkl9012mnop3456qrst7890uvwx==
```

### 4. Install python-dotenv

```bash
python3 -m pip install python-dotenv
```

### 5. Test It

```bash
python3 test_installation.py
```

If everything is set up correctly, all tests should pass!

## Free Tier Limits

Picovoice free tier includes:
- ✅ Unlimited local wake word detection
- ✅ Up to 3 custom wake words
- ✅ Personal use only (commercial use requires paid plan)

## Troubleshooting

### "Invalid access key" Error

- Make sure you copied the entire access key (including `==` at the end)
- Check for extra spaces or quotes in the `.env` file
- Make sure the `.env` file is in the project root directory

### Can't Find Access Key

1. Log in to https://console.picovoice.ai/
2. Click on your profile (top right)
3. Look for "Access Keys" or "API Keys"
4. Copy the key shown

### Still Having Issues?

- Try creating a new access key in the console
- Make sure you're logged into the correct account
- Contact Picovoice support: https://picovoice.ai/support/

---

**Note:** Keep your access key private! Don't share it publicly or commit it to version control.
