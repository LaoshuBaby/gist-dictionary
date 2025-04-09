import json
import os

import fastapi
import uvicorn

from auth import get_token
from basic import init_config
from gist import get_gist
from log import logger


def init():
    """
    在经过init之后，就已经获得了authentication的token了
    """
    logger.info("Hello World!")
    config = init_config()
    token = get_token()
    gist_raw_data = get_gist(auth_token=token, gist_id="")
    pass

    pass


def main():
    config = init()


if __name__ == "__main__":
    main()
