#!/bin/bash

echo "🛑 Removing Sage Auto-Start..."

# Stop the service
echo "Stopping Sage..."
launchctl stop com.sage.assistant

# Unload the LaunchAgent
echo "Unloading LaunchAgent..."
launchctl unload ~/Library/LaunchAgents/com.sage.assistant.plist

# Remove the plist file
echo "Removing LaunchAgent file..."
rm ~/Library/LaunchAgents/com.sage.assistant.plist

echo "✅ Sage auto-start has been removed!"
echo ""
echo "Sage will no longer start automatically."
echo "You can still run it manually with: python3 main.py"
