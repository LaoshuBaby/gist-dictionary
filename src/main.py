import json
import os

import fastapi
import requests
import uvicorn


def init():
    # 交互式填写必要信息和创建config
    # 用户需要的gist需要自己手动创建好，本工具不会也不能为用户代办这个操作，以及这样可以保证在生成github token的时候授予最小权限即只能读写一个gist就可以用
    pass


def get_config():
    with open(".gist_dictionary.json", "r", encoding="utf-8") as f:
        config = json.loads(f.read())
    pass


def get_gist_content():
    # 需要获取的gist名字需要提前放在配置文件里面，建议写一个init过程
    # 这块的读取文档在 https://docs.github.com/en/rest/gists/gists?apiVersion=2022-11-28#get-a-gist

    pass


def put_gist_content():
    pass


def authentication():

    # 获取gist访问的时候需要一个github的token，这个可以从系统环境变量去获得，并且不推荐明文存储在任何文件中因为这个太危险了。
    # 其实系统环境变量也是非常危险的
    # 还是优先看有没有github官方指定的环境变量名，有，https://cli.github.com/manual/gh_help_environment

    print(os.environ.get("GH_TOKEN", None))
    pass


def main():
    authentication()
    pass


if __name__ == "__main__":
    main()
