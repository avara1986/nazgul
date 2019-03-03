import json
import logging

from flask import jsonify

from nazgul.action import ActionManager
from nazgul.constants import LOGGER_NAME
from nazgul.message import MessageManager

logger = logging.getLogger(LOGGER_NAME)


class App(object):

    def run(self, request):
        logger.info("Recived message:")
        logger.info(json.dumps(request.get_json(), ensure_ascii=False))

        message = MessageManager(trigger_object=request, path=__file__).get()
        if not message:
            return jsonify({
                "payload": {
                    "google": {
                        "expectUserResponse": True,
                        "richResponse": {
                            "items": [
                                {
                                    "simpleResponse": {
                                        "displayText": "No te entiendo",
                                        "textToSpeech": "No te entiendo"
                                    }
                                }
                            ]
                        }
                    }
                }
            })

        action = ActionManager(trigger_object=message, path=__file__)
        return message.response(text=action.response()).json()
