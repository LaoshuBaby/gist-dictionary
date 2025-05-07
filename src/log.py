"""
Logger configuration for the gist-dictionary application.

This module configures the application logger using hellologger.
"""
import os

from hellologger import get_logger

from const import ROOT_PATH

# Configure the application logger
logger = get_logger(
    log_path=os.path.join(ROOT_PATH, "log"),
    log_file="gist_dictionary_{time}.log",
    log_target={
        "local": True,
        "aliyun": False,
        "aws": False,
    },
    log_level={
        "local": "TRACE",
        "aliyun": "INFO",
    },
)
