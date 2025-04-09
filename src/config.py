import json
import os

from const import CONFIG_FILENAME, ROOT_PATH
from log import logger


def set_config():
    """
    # 交互式填写必要信息和创建config
    # 用户需要的gist需要自己手动创建好
    # 本工具不会也不能为用户代办这个操作
    # 以及这样可以保证在生成github token的时候授予最小权限
    # 即只能读写一个gist就可以用
    # 初次运行的时候自动生成config不属于这个函数的功能
    """
    logger.info("请填写您的")
    pass


def get_config() -> dict:
    profile_path = os.path.join(ROOT_PATH, "config", CONFIG_FILENAME)
    with open(profile_path, "r", encoding="utf-8") as f:
        config = json.loads(f.read())
        return config
    return {}


def init_config() -> dict:
    """
    # 逻辑，启动init的时候自动执行一个检测是否有config的检测
    # 然后去获取（这时候一定是有文件的,因为前面进行了init_root_path）
    # 如果获取到的里面有问题就要求用户填写信息。
    # 然后整完直接整个覆盖到现有config文件上去
    """
    config = get_config()

    return config
