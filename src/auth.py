import json
import os

from const import CONFIG_FILENAME, ROOT_PATH
from log import logger


def get_token() -> str:
    # 获取gist访问的时候需要一个github的token

    # 在读取环境变量名称的时候将优先github官方指定的环境变量名
    # https://cli.github.com/manual/gh_help_environment
    # 首先是系统环境变量
    # 其次才是读取指定文件
    # 但这是非常危险的，不推荐这么做

    try:
        GH_TOKEN = os.environ.get("GH_TOKEN", None)
        GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
        logger.debug(GH_TOKEN)
        logger.debug(GITHUB_TOKEN)
        if GH_TOKEN != None and GH_TOKEN != "":
            token = GH_TOKEN
        elif GITHUB_TOKEN != None and GITHUB_TOKEN != "":
            token = GITHUB_TOKEN
        else:
            with open(
                os.path.join(ROOT_PATH, "config", CONFIG_FILENAME),
                "r",
                encoding="utf-8",
            ) as f:
                token = json.loads(f.read().replace("\n", "")).get("GH_TOKEN", "")

    except Exception as e:
        logger.error(e)
        with open(
            os.path.join(ROOT_PATH, "config", CONFIG_FILENAME),
            "r",
            encoding="utf-8",
        ) as f:
            token = json.loads(f.read().replace("\n", "")).get("GH_TOKEN", "")

    logger.success(token)
    return token
