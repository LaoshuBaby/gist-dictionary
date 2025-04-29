import json
import os

from const import ROOT_FOLDERS, ROOT_PATH, ROOT_PROFILES
from log import logger


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
        this_profile_path = os.path.join(ROOT_PATH, "config", profile)
        if os.path.exists(this_profile_path) != True:
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
