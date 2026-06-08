from Logs import logger
import json
import re
import requests
from fastapi import FastAPI, Request
from app.config.settings import settings
from app.services.llm_router import llm_router
from app.core.tools import tool_engine
app = FastAPI()

conversation_history = {}
active_voices = {}

def execute_tools(chat_id, tool_calls):
    system_messages = []
    for tool_call in tool_calls:
        try:
            args = json.loads(tool_call.function.arguments)
            if tool_call.function.name == "change_voice":
                voice_name = args.get("voice_name")
                voice_id = tool_engine.available_voices.get(voice_name, "en-US-AvaNeural")
                active_voices[chat_id] = voice_id
                logging.info(f"Voice changed to {voice_id} for {chat_id}")
                system_messages.append({"role": "system", "content": f"Tool execution successful: Voice changed to {voice_name}. Acknowledge this."})
            
            elif tool_call.function.name == "send_voice_note":
                text = args.get("text")
                voice_id = active_voices.get(chat_id, "en-US-AvaNeural")
                # Need to use subprocess to run edge-tts
                import subprocess
                import os
                output_file = os.path.abspath(f"voicenote_{chat_id}.mp3")
                subprocess.run(["edge-tts", "--text", text, "--voice", voice_id, "--write-media", output_file], check=True)
                
                # Ping text_agent_vps to send it
                requests.post(f"{settings.TEXT_AGENT_URL}/send_file", json={"chatId": chat_id, "filePath": output_file})
                system_messages.append({"role": "system", "content": "Tool execution successful: Voice note sent."})
        except Exception as e:
            logging.error(f"Tool execution failed: {e}")
            system_messages.append({"role": "system", "content": f"Tool execution failed: {e}"})
    return system_messages

async def call_llm_with_tools(messages, chat_id):
    """Recursive wrapper over llm_router to handle tool execution."""
    msg = await llm_router.call_llm(messages, tools=tool_engine.get_tool_definitions())
    
    if msg and hasattr(msg, 'choices') and msg.choices:
        response_msg = msg.choices[0].message
        
        if hasattr(response_msg, 'tool_calls') and response_msg.tool_calls:
            # Append the assistant's tool call message
            messages.append(response_msg)
            tool_results = execute_tools(chat_id, response_msg.tool_calls)
            for res in tool_results:
                messages.append(res)
            return await call_llm_with_tools(messages, chat_id)
            
        return response_msg.content
    return "Error communicating with AI Providers."

@app.post("/webhook")
async def receive_webhook(request: Request):
    payload = await request.json()
    chat_id = payload.get("chatId")
    text_body = payload.get("text", "")
    
    if not chat_id or not text_body:
        return {"status": "ignored"}
        
    if chat_id not in conversation_history:
        conversation_history[chat_id] = [{"role": "system", "content": "You are a helpful WhatsApp AI assistant named ZT002. For your very first message, you MUST introduce yourself to the user enthusiastically."}]
        
    conversation_history[chat_id].append({"role": "user", "content": text_body})
    
    reply = await call_llm_with_tools(conversation_history[chat_id], chat_id)
    
    # Catch and remove hallucinated XML tags from LLaMA before sending to WhatsApp
    reply = re.sub(r'<[^>]+>.*?</[^>]+>', '', reply, flags=re.DOTALL).strip()
    
    conversation_history[chat_id].append({"role": "assistant", "content": reply})
    
    requests.post(f"{settings.TEXT_AGENT_URL}/send", json={"chatId": chat_id, "text": reply})
    return {"status": "success"}

@app.post("/voice_chat")
async def receive_voice_chat(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    chat_id = "voice_caller"
    
    if chat_id not in conversation_history:
        conversation_history[chat_id] = [
            {"role": "system", "content": "You are a friendly AI named ZT002. Keep answers short (1-2 sentences). For your very first response, you MUST excitedly introduce yourself to the user."}
        ]
        
    conversation_history[chat_id].append({"role": "user", "content": text})
    
    reply = await call_llm_with_tools(conversation_history[chat_id], chat_id)
    
    # Catch hallucinated XML tags from LLaMA models
    tool_match = re.search(r'<function=([^>]+)>({.*?})</function>', reply)
    if tool_match:
        try:
            func_name = tool_match.group(1)
            args = json.loads(tool_match.group(2))
            if func_name == "change_voice":
                voice_name = args.get("voice_name", "ava")
                active_voices[chat_id] = tool_engine.available_voices.get(voice_name, "en-US-AvaNeural")
        except:
            pass
        reply = re.sub(r'<function=.*?</function>', '', reply).strip()
        
    conversation_history[chat_id].append({"role": "assistant", "content": reply})
    current_voice = active_voices.get(chat_id, "en-US-AvaNeural")
    return {"reply": reply, "voice": current_voice}

@app.get("/")
def read_root():
    return {"status": "Enterprise AI Router is online!"}
