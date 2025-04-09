import requests

from log import logger

# 1
# 需要注意的是，这里是我自己实现的GitHub Gist API
# 当然这种库绝对是已经有了的
# 因此后续更多时候还是用其他库，除非出错才会用自带库重试
# 2
# 需要获取的gist名字推荐提前放在配置文件里面，建议写一个init过程
# 这块的读取文档在 https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist

IMPLEMENT="local"

# Optional value:
# "local": 
# * impl made by me
# "witherredaway": 
# * PyPi-[github-gists](https://pypi.org/project/github-gists/)
# * GitHub-[WitherredAway/gists.py](https://github.com/WitherredAway/gists.py)


def get_gist(auth_token: str, gist_id: str):

    if IMPLEMENT == "local":
        url = f"https://api.github.com/gists/{gist_id}"

        headers = {
            "Authorization": f"token {auth_token}",
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

        gist_data=gist_metadata.get("files").get("wordbank.json").get("content")
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
    return gist_data


def put_gist():
    pass
