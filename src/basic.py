import os

from hellologger import get_logger

ROOT_PATH = os.path.join(os.environ["USERPROFILE"], ".gist_dictionary")


ROOT_FOLDERS = ["log", "config"]
ROOT_PROFILES = ["gist_dictionary.json"]


CONFIG_FILENAME = "gist_dictionary.json"


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


def init_root_path() -> None:

    # root check
    if os.path.exists(ROOT_PATH) != True:
        os.mkdir(ROOT_PATH)
    # folder check
    for folder in ROOT_FOLDERS:
        this_folder_path = os.path.join(ROOT_PATH, folder)
        if os.path.exists(this_folder_path) != True:

            os.mkdir(this_folder_path)
    # profile files check

    for profile in ROOT_PROFILES:
        this_profile_path = os.path.join(ROOT_PROFILES, "config", profile)
        if os.path.exists(this_profile_path) != True:
            import json

            with open(
                this_profile_path, "w", encoding="utf-8"
            ) as f_this_profile:
                f_this_profile.write(
                    json.dumps(
                        {
                            "GH_TOKEN": "DO NOT CONTAIN THIS",
                            "config": {"gist_name": ""},
                        },
                        ensure_ascii=False,
                        indent=2,
                        sort_keys=False,
                    )
                )


def get_root_path() -> str:
    init_root_path()
    return ROOT_PATH