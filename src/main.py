import json
import os

import fastapi
import uvicorn

from auth import get_token
from config import init_config
from gist import get_gist
from log import logger


def init()->dict:
    """
    在经过init之后，就已经获得了authentication的token了
    """
    logger.info("Hello World!")
    config = init_config()
    config["GH_TOKEN"] = get_token()
    logger.debug(config)
    return config


def main():
    config = init()
    gist_raw_data = get_gist(auth_token=config["GH_TOKEN"], gist_id="")
    logger.info(gist_raw_data)

if __name__ == "__main__":
    main()
