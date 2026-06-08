# This is the root entrypoint for the Desktop Voice Agent.
# It programmatically boots the Enterprise FastAPI Server located in app/main.py

import uvicorn
from app.main import app

if __name__ == "__main__":
    print("===============================================")
    print("   STARTING WHATSAPP BRAIN SERVER (DESKTOP)   ")
    print("===============================================")
    uvicorn.run(app, host="0.0.0.0", port=8000)
