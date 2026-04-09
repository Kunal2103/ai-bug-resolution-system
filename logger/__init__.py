import logging
import os
from datetime import datetime

# Create a logs directory at the root level if it doesn't exist
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Define the log file name using the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

logging.basicConfig(
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("AI_Bug_Resolution_System")