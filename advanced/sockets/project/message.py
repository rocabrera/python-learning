import json


class Message:

    def __init__(self, msg):
        self.msg = msg

    def to_json(self, encoding=None):

        if encoding == "utf-8":
            return json.dumps({"message": self.msg}).encode(encoding)

        return json.dumps({"message": self.msg})
