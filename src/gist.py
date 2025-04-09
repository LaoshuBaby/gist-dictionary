import requests

from log import logger

# 1
# 需要注意的是，这里是我自己实现的GitHub Gist API
# 当然这种库绝对是已经有了的
# 因此后续更多时候还是用其他库，除非出错才会用自带库重试
# 2
# 需要获取的gist名字推荐提前放在配置文件里面，建议写一个init过程
# 这块的读取文档在 https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist


def get_gist(auth_token: str, gist_id: str):

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
        gist_data = response.json()
        print(gist_data)
    else:
        print(f"Failed to retrieve gist: {response.status_code}")
        print(response.text)


def put_gist():
    pass
