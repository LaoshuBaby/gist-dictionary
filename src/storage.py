"""
Storage initialization and management for the gist-dictionary application.
"""
import os

from const import ROOT_FOLDERS, ROOT_PATH, ROOT_PROFILES
from log import logger
from utils import write_json_file


def init_root_path() -> None:
    """
    Initialize the application directory structure and default configuration files.
    """
    # Create root directory if it doesn't exist
    if not os.path.exists(ROOT_PATH):
        os.makedirs(ROOT_PATH, exist_ok=True)
        logger.info(f"Created root directory: {ROOT_PATH}")

    # Create required folders
    for folder in ROOT_FOLDERS:
        folder_path = os.path.join(ROOT_PATH, folder)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Created directory: {folder_path}")

    # Create default profile files
    for profile in ROOT_PROFILES:
        profile_path = os.path.join(ROOT_PATH, "config", profile)
        if not os.path.exists(profile_path):
            default_config = {
                "GH_TOKEN": "DO NOT CONTAIN THIS",
                "config": {"gist_name": ""},
            }
            write_json_file(profile_path, default_config)
            logger.info(f"Created default configuration file: {profile_path}")
