class GoogleChatMessage(object):
    user = ""
    user_id = ""
    text = ""

    def __init__(self, request):
        self.msg = self.parse_request(request)
        self.user = self.msg["user"]["displayName"]
        self.user_id = self.msg["user"]["name"]
        self.text = self.msg["message"]["text"]

    def parse_request(self, request):
        msg = request.get_json()
        return msg
