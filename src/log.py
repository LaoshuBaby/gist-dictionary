from hellologger import get_logger

logger = get_logger(
    log_path=os.path.join(get_root_path(), "log"),
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
