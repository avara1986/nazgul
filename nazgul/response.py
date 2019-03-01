from flask import jsonify


class GoogleChatResponse(object):
    def __init__(self, *args, **kwargs):
        self.response = kwargs

    def json(self, *args, **kwargs):
        return jsonify(self.response)
