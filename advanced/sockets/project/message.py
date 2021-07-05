import json


class Message:

    def __init__(self, msg, type_msg, filename=None, info=None):
        self.msg = msg  # Mensagem a passar
        self.type_msg = type_msg  # tipos de msg: AWAIT, OK, INFO
        self.filename = filename
        self.info = info

    def to_json(self, encoding=None):

        dict_msg = {"type_msg": self.type_msg,
                    "message": self.msg,
                    "info": self.info,
                    "file": self.filename}

        if encoding == "utf-8":
            return json.dumps(dict_msg).encode(encoding)

        return json.dumps(dict_msg)
