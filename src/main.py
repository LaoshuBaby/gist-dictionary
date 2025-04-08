import json
import os

import fastapi
import requests
import uvicorn

import hellologger

from hellologger import get_logger


def get_yuheng_path() -> str:
    YUHENG_PATH = os.path.join(os.environ["USERPROFILE"], ".yuheng")

    def init_yuheng_path() -> None:
        YUHENG_FOLDER = ["cache", "db_profiles", "log"]
        YUHENG_PROFILES = [
            "mysql.db_profiles.yuheng",
            "postgresql.db_profiles.yuheng",
        ]
        # root check
        if os.path.exists(YUHENG_PATH) != True:
            print("[YUHENG ENVIRON INIT]", YUHENG_PATH, "isn't exist!")
            os.mkdir(YUHENG_PATH)
        # folder check
        for folder in YUHENG_FOLDER:
            this_folder_path = os.path.join(YUHENG_PATH, folder)
            if os.path.exists(this_folder_path) != True:
                print(
                    "[YUHENG ENVIRON INIT]", this_folder_path, "isn't exist!"
                )
                os.mkdir(this_folder_path)
        # profile files check
        for profile in YUHENG_PROFILES:
            this_profile_path = os.path.join(
                YUHENG_PATH, "db_profiles", profile
            )
            if os.path.exists(this_profile_path) != True:
                import json

                print(
                    "[YUHENG ENVIRON INIT]", this_profile_path, "isn't exist!"
                )
                with open(
                    this_profile_path, "w", encoding="utf-8"
                ) as f_this_profile:
                    f_this_profile.write(
                        json.dumps(
                            {
                                "yuheng_doctype": "db_profile",
                                "_WARNING": "PLEASE DELETE THIS LINE AND FILL IT ACCORDING TO DOCS.",
                            }
                        )
                    )

    init_yuheng_path()
    return YUHENG_PATH



logger = get_logger(
    log_path=os.path.join(get_yuheng_path(), "log"),
    log_file="log_{time}.log",
    log_target={
        "local": True,
        "aliyun": False,
        "aws": False,
    },
    log_level={
        "local": "TRACE",
        "aliyun": "INFO",
    },
    **{**log_config_local, **log_config_aliyun},
)

CONFIG_FILENAME = ".gist_dictionary.json"


class Entry():
    def __init__(self):
        self.attribute={"type":"entry"}
        pass

    def __attach_attribute():
        pass

def init_config()->dict:
    # 交互式填写必要信息和创建config
    # 用户需要的gist需要自己手动创建好
    # 本工具不会也不能为用户代办这个操作
    # 以及这样可以保证在生成github token的时候授予最小权限
    # 即只能读写一个gist就可以用
    set_config()
    config=get_config()
    # 逻辑，启动init的时候自动执行一个检测是否有config的检测
    # 然后去获取（这时候一定是有文件的）
    # 如果获取到的里面有问题就要求用户填写信息。
    # 然后整完直接整个覆盖到现有config文件上去
    return config


def get_config() -> dict:
    with open(CONFIG_FILENAME, "r", encoding="utf-8") as f:
        config = json.loads(f.read())
        return config
    return {}


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


def authentication(token:str=""):

    # 获取gist访问的时候需要一个github的token，这个可以从系统环境变量去获得，并且不推荐明文存储在任何文件中因为这个太危险了。
    # 其实系统环境变量也是非常危险的
    # 还是优先看有没有github官方指定的环境变量名，有，https://cli.github.com/manual/gh_help_environment
    try:
        GH_TOKEN=os.environ.get("GH_TOKEN",None)
        GITHUB_TOKEN =os.environ.get("GITHUB_TOKEN",None)
        if GH_TOKEN!=None and GH_TOKEN!="":
            TOKEN=GH_TOKEN
        elif GITHUB_TOKEN!=None and GITHUB_TOKEN!="":
            TOKEN=GITHUB_TOKEN
        else:
            TOKEN=token
    except Exception as e:
        print(e)
        TOKEN=token

    print(TOKEN)
    pass


def main():
    # init_config=init()
    config=init_config()
    # print(config)
    if config.get("GH_TOKEN",None)!=None:
        TOKEN=config["GH_TOKEN"]
        # print(TOKEN)
    authentication(token=TOKEN)
    pass


if __name__ == "__main__":
    main()
