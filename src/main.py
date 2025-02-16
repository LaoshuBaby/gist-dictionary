import json
import os

import fastapi
import requests
import uvicorn

CONFIG_FILENAME = ".gist_dictionary.json"


def init():
    # 交互式填写必要信息和创建config
    # 用户需要的gist需要自己手动创建好，本工具不会也不能为用户代办这个操作，以及这样可以保证在生成github token的时候授予最小权限即只能读写一个gist就可以用
    set_config()
    get_config()
    # 逻辑，启动init的时候自动执行一个检测是否有config的检测，然后去获取（这时候一定是有文件的），如果获取到的里面有问题就要求用户填写信息。
    # 然后整完直接整个覆盖到现有config文件上去


def get_config() -> dict:
    with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
        config = json.loads(f.read())


def set_config(config_dict: dict = {}) -> None:
    DEFAULT_CONFIG = """
{
  "GH_TOKEN": "DO NOT CONTAIN THIS",
  "config": {
    "gist_name": ""
  }
}
"""
    if os.path.exists(CONFIG_FILENAME) is False:
        with open(CONFIG_FILENAME, "w", encoding="utf-8") as f:
            f.write(DEFAULT_CONFIG)


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
