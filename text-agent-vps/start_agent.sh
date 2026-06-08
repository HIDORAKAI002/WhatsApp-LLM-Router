#!/bin/sh
echo "==============================================="
echo "   STARTING WHATSAPP TEXT AGENT (VPS MODULE)"
echo "==============================================="

echo "Installing Node dependencies..."
npm install

echo "Starting Text Agent via Node..."
node src/index.js
