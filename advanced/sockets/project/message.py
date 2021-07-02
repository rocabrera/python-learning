import json


class Message:

    def __init__(self, msg, type_msg):
        self.msg = msg  # Mensagem a passar
        self.type_msg = type_msg  # tipos de msg: AWAIT, OK, INFO

    def to_json(self, encoding=None):

        if encoding == "utf-8":
            return json.dumps({"type_msg": self.type_msg, "message": self.msg}).encode(encoding)

        return json.dumps({"type_msg": self.type_msg, "message": self.msg})
