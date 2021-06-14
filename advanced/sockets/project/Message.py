
class Message:

    def __init__(self,msg):
        self.msg = msg

    def transform(self):
        return self.msg.encode("ascii")