import json
import os

import uvicorn

from auth import get_token
from config import init_config
from entry import Entry
from gist import get_gist, update_gist
from log import logger
from storage import init_root_path

ENTRY_WORLD = set()


def init() -> dict:
    """
    will get config as return
    If can't get token from system path, auth module will use config inlined token value.

    Note that this is unsafe and dangerous.
    """
    logger.success("Hello World!")
    init_root_path()
    config = init_config()
    config["GH_TOKEN"] = get_token()
    logger.debug(f"config: \n{config}")
    return config


def main():
    """
    default word storage is a global list for Entry's obj
    while you can get plain text list with server api
    """
    config = init()
    gist_raw_data = get_gist(
        auth_token=config["GH_TOKEN"], gist_id=config["config"]["gist_name"]
    )
    logger.info(f"gist_raw_data: \n{gist_raw_data}")
    logger.trace(type(gist_raw_data))
    gist_data = json.loads(gist_raw_data)
    for word in gist_data.get("wordbank"):
        temp = Entry(word["word"])
        logger.info(temp._get())
        ENTRY_WORLD.add(temp)
    update_gist(
        auth_token=config["GH_TOKEN"],
        gist_id=config["config"]["gist_name"],
        gist_data=gist_raw_data + gist_raw_data,
    )

    # uvicorn.run(app=app)


if __name__ == "__main__":
    main()
