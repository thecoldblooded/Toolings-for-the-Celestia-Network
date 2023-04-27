import os, sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# telegram
ENV = os.getenv('ENV')
API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

if not API_TOKEN:
    print('Please read README first!')
    sys.exit(0)

SLEEP_TIME = 60

# chain
CHAIN_ENDPOINT = os.getenv('CHAIN_ENDPOINT')
AUTO_RECOVER = os.getenv('AUTO_RECOVER')
MOUNT_POINT = os.getenv('MOUNT_POINT')

# system
DISK_LIMIT = int(os.getenv('DISK_LIMIT', 0))
RAM_LIMIT = int(os.getenv('RAM_LIMIT', 0))
CPU_LIMIT = int(os.getenv('CPU_LIMIT', 0))
LOG_SIZE_THRESHOLD = os.getenv('LOG_SIZE_THRESHOLD')

# bash
HAS_TIMEOUT = True


class Emoji:
    START = '\U0001F514'
    RAM = '\U0001F4A5'
    CPU = '\U000026A0'
    DISK = '\U0001F4BE'
    STUCK = '\U000026D4'
    BLOCK_MISS = '\U0000274C'
    RPC_FAILED = '\U000026A0'
    SLOW = '\U0001f40c'
    SYNC_OK = '\U00002705'
    BANDWIDTH = '\U0001F7E2'
    STATE_AMOUNT = '\U0001F4E2'
