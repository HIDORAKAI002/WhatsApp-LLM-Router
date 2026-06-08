import subprocess
import sys

if __name__ == "__main__":
    print("===============================================")
    print("   STARTING WHATSAPP TEXT AGENT (VPS)          ")
    print("===============================================")
    
    try:
        print("Installing NPM Dependencies...")
        subprocess.run(["npm", "install"], shell=True, check=True)
            
        print("\nStarting NodeJS server...")
        subprocess.run(["npm", "start"], shell=True, check=True)
        
    except KeyboardInterrupt:
        print("\nShutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"\nCRITICAL ERROR: {e}")
        sys.exit(1)
