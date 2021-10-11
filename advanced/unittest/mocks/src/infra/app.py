from flask import Flask, Response, request

app = Flask(__name__)

def _save_file(path) -> None:

    with open(path, "wb") as f:
        pass