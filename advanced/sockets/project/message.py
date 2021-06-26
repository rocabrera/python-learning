import json
import sys


class Message:

    def __init__(self, msg):
        self.msg = msg

    def to_json(self):
        return json.dumps({"message": self.msg})


if __name__ == "__main__":

    try:
        sys.exit("Meu deus")
    except SystemExit as e:
        print(e)
        print("OLA")
