import os
from Logs import logger
import io
import time
import sys
import threading
import base64
import requests
import numpy as np
import soundcard as sc
import soundfile as sf
import pyautogui
from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import pygame

print("=========================================")
print("Booting up Desktop Agent (Please wait...)")
print("=========================================")

# Initialize PyGame mixer for playing MP3s directly to the Virtual Cable
import pygame._sdl2.audio as sdl2_audio
pygame.mixer.init() # Initial init to load SDL
pygame.mixer.quit() # Quit to reinit with specific device
pygame.mixer.init(devicename='CABLE Input (VB-Audio Virtual Cable)')

# Load env
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
GROQ_KEY = os.getenv("GROQ_API_KEYS", "").split(",")[0]
groq_client = OpenAI(api_key=GROQ_KEY, base_url="https://api.groq.com/openai/v1")

# Audio config
SAMPLE_RATE = 16000
CHUNK_SIZE = 1024
SILENCE_THRESHOLD = 0.005  # Raised to ignore static noise
SILENCE_DURATION = 0.35

call_active = False

import re
import queue
import threading
import os

def generate_and_play_edge_tts(text: str, voice: str):
    print(f"Streaming voice via Edge-TTS...", flush=True)
    
    # Split text into sentences for streaming playback
    sentences = re.split(r'(?<=[.!?]) +', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return

    audio_queue = queue.Queue()
    
    def generator_thread():
        for i, sentence in enumerate(sentences):
            output_file = f"response_part_{i}.mp3"
            try:
                subprocess.run(["edge-tts", "--text", sentence, "--voice", voice, "--write-media", output_file], check=True)
                audio_queue.put(output_file)
            except Exception as e:
                print(f"TTS Error on sentence {i}: {e}")
        audio_queue.put(None) # EOF marker
        
    t = threading.Thread(target=generator_thread)
    t.start()
    
    # Playback loop
    while True:
        try:
            file_to_play = audio_queue.get(timeout=15)
            if file_to_play is None:
                break
                
            pygame.mixer.music.load(file_to_play)
            pygame.mixer.music.play()
            
            # Wait for this sentence to finish before playing the next
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
                
            pygame.mixer.music.unload()
            
            # Clean up the temp file
            try:
                os.remove(file_to_play)
            except:
                pass
        except queue.Empty:
            print("Audio streaming timeout.")
            break
            
    print("Audio playback complete.", flush=True)

def transcribe_audio(audio_data):
    print("Transcribing with Groq Whisper...")
    wav_io = io.BytesIO()
    sf.write(wav_io, audio_data, SAMPLE_RATE, format='WAV', subtype='PCM_16')
    wav_io.seek(0)
    
    wav_io.name = "audio.wav"
    try:
        # We can use the fast groq whisper model for zero latency transcription
        transcription = groq_client.audio.transcriptions.create(
            file=(wav_io.name, wav_io.read()),
            model="whisper-large-v3",
            prompt="Keep punctuation."
        )
        return transcription.text
    except Exception as e:
        print(f"Transcription error: {e}")
        return ""

def ask_llm(user_text):
    try:
        response = requests.post("http://localhost:8000/voice_chat", json={"text": user_text})
        if response.status_code == 200:
            data = response.json()
            return data.get("reply", "Sorry, I missed that."), data.get("voice", "en-US-JennyNeural")
        return "Sorry, the brain is offline.", "en-US-JennyNeural"
    except Exception as e:
        print(f"Error calling main.py: {e}", flush=True)
        return "Sorry, I lost my train of thought.", "en-US-JennyNeural"

# Common Whisper hallucinations when fed pure silence or static
WHISPER_HALLUCINATIONS = [
    "Thank you.", "Thank you", "Hasta luego.", "Hasta luego", 
    "Bye.", "You", "Okay.", "Subtitles by", "beep", "Beep"
]

def start_loopback_listener():
    try:
        # 100% reliable: Use the system default speaker loopback
        default_speaker = sc.default_speaker()
        target_mic = sc.get_microphone(id=default_speaker.id, include_loopback=True)
        print(f"Listening to caller audio on System Default: {target_mic.name}")
        
    except Exception as e:
        print(f"Failed to get loopback: {e}")
        return

    print("Voice AI activated. Waiting for caller to speak...")
    with target_mic.recorder(samplerate=SAMPLE_RATE) as recorder:
        buffer = []
        silent_frames = 0
        recording = False
        
        while call_active:
            chunk = recorder.record(numframes=SAMPLE_RATE // 10)
            mono_chunk = np.mean(chunk, axis=1)
            vol = np.max(np.abs(mono_chunk))
            
            # Debug: print volume every second so we know it's not dead
            if not hasattr(recorder, "debug_counter"):
                recorder.debug_counter = 0
            recorder.debug_counter += 1
            if recorder.debug_counter % 10 == 0 and not recording:
                print(f"[Debug] Current audio volume level: {vol:.5f} (Needs to hit > {SILENCE_THRESHOLD} to trigger)")
            
            if vol > SILENCE_THRESHOLD:
                if not recording:
                    print("\nCaller is speaking...")
                    recording = True
                buffer.append(mono_chunk)
                silent_frames = 0
            else:
                if recording:
                    buffer.append(mono_chunk)
                    silent_frames += 1
                    if silent_frames > (SILENCE_DURATION * 10):
                        print("Silence detected. Processing audio...")
                        recording = False
                        full_audio = np.concatenate(buffer)
                        buffer = []
                        silent_frames = 0
                        text = transcribe_audio(full_audio)
                        
                        if text:
                            clean_text = text.strip()
                            is_hallucination = any(h.lower() in clean_text.lower() for h in WHISPER_HALLUCINATIONS)
                            if len(clean_text) <= 2 or (is_hallucination and len(clean_text) < 15):
                                print(f"Ignored static/hallucination: {clean_text}")
                            else:
                                print(f"Caller said: {text}")
                                reply, voice = ask_llm(text)
                                print(f"Bot reply: {reply} [Voice: {voice}]")
                                generate_and_play_edge_tts(reply, voice)
                        else:
                            print("Ignored empty speech/noise.")

def monitor_screen_for_call():
    global call_active
    
    if not os.path.exists("accept.png"):
        print("\n" + "!"*60)
        print("CRITICAL ERROR: 'accept.png' is MISSING!")
        print("You must save the green Accept button image as 'accept.png'")
        print("directly inside the whatsapp_agent folder before running this.")
        print("!"*60 + "\n")
        sys.exit(1)
        
    print("======================================================")
    print("Scanning screen for 'accept.png' (WhatsApp Accept Button)...")
    print("Leave the WhatsApp Desktop app visible on your screen.")
    print("======================================================")
    
    while True:
        if not call_active:
            try:
                # Require opencv-python installed for confidence keyword
                button_pos = pyautogui.locateOnScreen("accept.png", confidence=0.8)
                if button_pos:
                    print("\n>>> INCOMING CALL DETECTED! <<<")
                    print("Moving mouse to click Accept...")
                    pyautogui.click(button_pos)
                    call_active = True
                    print("Call Answered! Starting audio loopback pipeline...")
                    time.sleep(1.5) # Wait for call connection
                    
                    # Start the audio listening loop in the main thread
                    start_loopback_listener()
            except pyautogui.ImageNotFoundException:
                pass
            except Exception as e:
                # Ignore random pyautogui errors
                pass
        time.sleep(1)

if __name__ == "__main__":
    monitor_screen_for_call()
