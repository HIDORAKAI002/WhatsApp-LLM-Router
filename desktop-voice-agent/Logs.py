import logging
import sys
import os

def setup_logger():
    logger = logging.getLogger("WhatsAppAgent")
    logger.setLevel(logging.DEBUG)
    
    # Prevent adding multiple handlers if setup_logger is called multiple times
    if not logger.handlers:
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # File Handler (Crash Log)
        log_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "agent_crashes.log"))
        file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
        file_handler.setLevel(logging.WARNING)  # Only log Warnings/Errors to file
        
        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
    return logger

logger = setup_logger()

# Global exception handler to log ALL crashes
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logger.critical("Uncaught Exception / Application Crash!", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception
