import os
import logging

raw_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
LOG_LEVEL = raw_level if raw_level in logging._nameToLevel else 'INFO'
LOG_LEVEL_INT = logging._nameToLevel[LOG_LEVEL]