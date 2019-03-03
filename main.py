import logging

from flask import Flask, request

from nazgul.app import App
from nazgul.constants import LOGGER_NAME

logger = logging.getLogger(LOGGER_NAME)


def nazgul_bot(request):
    app = App()
    return app.run(request)


if __name__ == "__main__":
    app = Flask(__name__)


    @app.route('/', methods=["GET", "POST"])
    def index():
        return nazgul_bot(request)


    app.run('127.0.0.1', 8000, debug=True)
