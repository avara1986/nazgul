from nazgul.action import ActionManager
from nazgul.response import GoogleChatResponse
from nazgul.message import GoogleChatMessage


def nazgul_bot(request):
    msg = GoogleChatMessage(request)
    action = ActionManager(message=msg, path=__file__)
    return GoogleChatResponse(text=action.response()).json()


if __name__ == "__main__":
    from flask import Flask, request

    app = Flask(__name__)


    @app.route('/', methods=["GET", "POST"])
    def index():
        return nazgul_bot(request)


    app.run('127.0.0.1', 8000, debug=True)
