class Entry:
    def __init__(self, word: str):
        self.attribute = {"type": "entry"}
        self.word = word
        pass

    def __attach_attribute(self):
        pass

    def _get(self):
        return self.word
