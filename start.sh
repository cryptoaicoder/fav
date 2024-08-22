#!/bin/bash
ollama serve &
sleep 10  # Wait for Ollama to start
ollama pull phi
python3 speech_assistant.py
