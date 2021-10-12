from flask import Flask, Response, request


app = Flask(__name__)


def _save_file(file) -> None:

    with open(path, "wb") as f:
        