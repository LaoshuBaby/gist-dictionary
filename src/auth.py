# 文件说明: 提取 Gist 访问 Token / File Description: Retrieves GitHub Gist access token from environment or config
# 文件说明: 提供 GitHub Gist 访问的 Token 获取功能 / File Description: Retrieves GitHub Gist access token from environment or config
# 文件说明: 提取 Gist 访问 Token / File Description: Retrieves GitHub Gist access token from environment or config

import json
# 文件说明: 提供 GitHub Gist 访问的 Token 获取功能 / File Description: Retrieves GitHub Gist access token from environment or config

import os

from const import CONFIG_FILENAME, ROOT_PATH
from log import logger


###

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from typing import Optional

# In a real application, this would be stored securely
API_KEYS = {"test_api_key": "admin"}

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)


async def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )
    
    # Check if the header has the correct format (Bearer <token>)
    if not api_key_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key format. Use 'Bearer <api_key>'",
        )
    
    # Extract the token
    api_key = api_key_header.replace("Bearer ", "")
    
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    
    return api_key

###

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
        logger.trace(f"GH_TOKEN = {GH_TOKEN}")
        logger.trace(f"GITHUB_TOKEN = {GITHUB_TOKEN}")
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
                token = json.loads(f.read().replace("\n", "")).get(
                    "GH_TOKEN", ""
                )

    except Exception as e:
        logger.error(e)
        with open(
            os.path.join(ROOT_PATH, "config", CONFIG_FILENAME),
            "r",
            encoding="utf-8",
        ) as f:
            token = json.loads(f.read().replace("\n", "")).get("GH_TOKEN", "")

    logger.success(f"token = {token}")
    return token
