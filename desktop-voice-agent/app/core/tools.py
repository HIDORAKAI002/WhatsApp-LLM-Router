import subprocess
import requests
import logging
from app.config.settings import settings

class ToolEngine:
    def __init__(self):
        self.available_voices = {
            "ana": "en-US-AnaNeural",
            "ava": "en-US-AvaNeural",
            "emma": "en-GB-EmmaNeural",
            "maisie": "en-GB-MaisieNeural",
            "guy": "en-US-GuyNeural",
            "andrew": "en-US-AndrewNeural"
        }
        
    def get_tool_definitions(self):
        return [
            {
                "type": "function",
                "function": {
                    "name": "change_voice",
                    "description": "Changes the voice of the AI agent dynamically.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "voice_name": {
                                "type": "string",
                                "enum": ["ana", "ava", "emma", "maisie", "guy", "andrew"],
                                "description": "The name of the new voice."
                            }
                        },
                        "required": ["voice_name"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "send_voice_note",
                    "description": "Generates a voice note mp3 and sends it to the user's WhatsApp chat. ONLY use this tool if the user EXPLICITLY asks for a voice message or audio response.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string", "description": "The exact text to speak in the voice note."}
                        },
                        "required": ["text"]
                    }
                }
            }
        ]

tool_engine = ToolEngine()
