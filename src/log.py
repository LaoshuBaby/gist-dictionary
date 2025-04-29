import os

from hellologger import get_logger

from const import ROOT_PATH

logger = get_logger(
    log_path=os.path.join(ROOT_PATH, "log"),
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
    **{"foo": "bar"},
)
