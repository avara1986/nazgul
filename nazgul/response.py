from flask import jsonify


class GoogleChatResponse(object):
    def __init__(self, text):
        self.response = text

    def json(self, *args, **kwargs):
        return jsonify({"text": self.response})


class GoogleActionResponse(object):
    def __init__(self, text):
        self.response = text

    def json(self, *args, **kwargs):
        return jsonify({
            "payload": {
                "google": {
                    "expectUserResponse": True,
                    "richResponse": {
                        "items": [
                            {
                                "simpleResponse": {
                                    "displayText": self.response,
                                    "textToSpeech": self.response
                                }
                            }
                        ]
                    }
                }
            }
        })
