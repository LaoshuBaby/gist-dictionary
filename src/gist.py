import json
from typing import Optional

import requests

from log import logger

# 1
# 需要注意的是，这里是我自己实现的GitHub Gist API
# 当然这种库绝对是已经有了的
# 因此后续更多时候还是用其他库，除非出错才会用自带库重试
# 2
# 需要获取的gist名字推荐提前放在配置文件里面，建议写一个init过程
# 这块的读取文档在 https://docs.github.com/en/rest/gists/gists

IMPLEMENT = "local"

# Optional value:
# "local":
# * impl made by me
# "witherredaway":
# * PyPi-[github-gists](https://pypi.org/project/github-gists/)
# * GitHub-[WitherredAway/gists.py](https://github.com/WitherredAway/gists.py)


def get_gist(auth_token: str, gist_id: str) -> Optional[str]:
    """
    Official API: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist
    """

    if IMPLEMENT == "local":
        url = f"https://api.github.com/gists/{gist_id}"

        headers = {
            "Accept": "application/vnd.github+jso",
            "Authorization": f"Bearer {auth_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        try:
            response = requests.get(url, headers=headers)
        except Exception as e:
            logger.error(e)

        if response.status_code == 200:
            gist_metadata = response.json()
            logger.trace(gist_metadata)
        else:
            logger.error(f"Failed to retrieve gist: {response.status_code}")
            logger.warning(response.text)

        gist_data = (
            gist_metadata.get("files").get("wordbank.json").get("content")
        )
    elif IMPLEMENT == "witherredaway":
        import asyncio

        import gists

        client = gists.Client()

        async def main_get():
            # Getting a gist does not require authorization

            # This method fetches the gist associated with the provided gist id, and returns a Gist object
            gist = await client.get_gist("GIST ID")
            return gist

        gist_data = asyncio.run(main_get())
    else:
        gist_data = None
    return gist_data


def update_gist(auth_token: str, gist_id: str, gist_data: str,file_name:str="wordbank.json"):
    """
    Official API: https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#update-a-gist
    """
    if IMPLEMENT == "local":

        url = f"https://api.github.com/gists/{gist_id}"

        headers = {
            "Accept": "application/vnd.github+jso",
            "Authorization": f"Bearer {auth_token}",
            "X-GitHub-Api-Version": "2022-11-28",
        }

        logger.trace(gist_data)

        gist_data_payload=json.loads('{"files":{"__FILE_NAME__":{"content":"__GIST_DATA__"}}}'.replace("__FILE_NAME__",file_name)
        )
        gist_data_payload["files"][file_name]["content"]=gist_data
        logger.trace(gist_data_payload)

        try:
            response = requests.patch(url, headers=headers,data=json.dumps(gist_data_payload,ensure_ascii=False,indent=0,sort_keys=False))
        except Exception as e:
            logger.error(e)

        if response.status_code == 200:
            logger.trace(response.text)
        else:
            logger.error(f"Failed to update gist: {response.status_code}")
            logger.warning(response.text)

        return response.status_code
    else:
        return None
