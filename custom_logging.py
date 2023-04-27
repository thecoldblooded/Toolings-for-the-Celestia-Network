import os
import logging
from logging import StreamHandler
from logging.handlers import TimedRotatingFileHandler
from constants import ENV

# Set up logging
if ENV == 'develop':
    log_handler = StreamHandler()
else:
    current_file_path = os.path.dirname(__file__)
    log_file_path = os.path.join(current_file_path, 'logs/tool.log')
    log_handler = TimedRotatingFileHandler(log_file_path, when='midnight', backupCount=30)
log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_handler.setFormatter(log_formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)
