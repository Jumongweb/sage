#!/bin/bash

echo "🚀 Setting up Sage Auto-Start..."

# Create logs directory
echo "Creating logs directory..."
mkdir -p /Users/macbook/Projects/jarvis/logs

# Copy plist to LaunchAgents
echo "Installing LaunchAgent..."
mkdir -p ~/Library/LaunchAgents
cp /Users/macbook/Projects/jarvis/com.sage.assistant.plist ~/Library/LaunchAgents/

# Load the LaunchAgent
echo "Loading LaunchAgent..."
launchctl load ~/Library/LaunchAgents/com.sage.assistant.plist

# Start the service
echo "Starting Sage..."
launchctl start com.sage.assistant

echo "✅ Sage auto-start has been configured!"
echo ""
echo "Sage will now start automatically when you log in."
echo "To check if it's running: launchctl list | grep sage"
echo "To view logs: tail -f /Users/macbook/Projects/jarvis/logs/sage.log"
echo ""
echo "To uninstall, run: ./uninstall_autostart.sh"
