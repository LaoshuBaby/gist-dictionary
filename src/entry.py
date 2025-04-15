class Entry:
    def __init__(self, word: str):
        self.attribute = {"type": "entry"}
        self.word = word
        pass

    def _attach_attribute(self):
        pass

    def _get(self):
        return self.word
    
    def _logline(self)->dict:
        return "everything in a one line json"
