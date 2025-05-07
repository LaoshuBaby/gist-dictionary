"""
Constants and configuration values for the gist-dictionary application.
"""
import os
import platform

# Determine the user's home directory based on the operating system
if platform.system() == "Windows":
    HOME_DIR = os.environ.get("USERPROFILE", os.path.expanduser("~"))
else:
    HOME_DIR = os.environ.get("HOME", os.path.expanduser("~"))

# Application paths
ROOT_PATH = os.path.join(HOME_DIR, ".gist_dictionary")
ROOT_FOLDERS = ["log", "config"]
ROOT_PROFILES = ["gist_dictionary.json"]
CONFIG_FILENAME = "gist_dictionary.json"

# API constants
API_VERSION = "v1"
DEFAULT_PORT = 12000

# Gist constants
DEFAULT_GIST_FILENAME = "wordbank.json"
