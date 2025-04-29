import json


class Entry:
    def __init__(self, word: str):
        self.attribute = {"type": "entry"}
        self.word = word
        pass

    def _attach_attribute(self):
        pass

    def _get(self):
        return self.word

    def _logline(self) -> dict:
        # get all attribute to json
        return json.dumps(
            "everything in a one line json",
            indent=0,
            ensure_ascii=True,
            sort_keys=False,
        )
