import json
import requests


class ultraChatBot():
    def __init__(self):
        # self.json = json
        # self.dict_messages = json['data']
        self.ultraAPIUrl = 'https://api.ultramsg.com/instance54817/'
        self.token = '02xe536u52jvb4z0'

    def listen(self):
        url = "https://api.ultramsg.com/instance54817/chats/messages"

        querystring = {
            "token": "02xe536u52jvb4z0",
            "chatId": "79635330968@c.us",
            "limit": 50
        }

        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, headers=headers, params=querystring)

        print(response.text)
        return response.text

    def send_requests(self, type, data):
        url = f"{self.ultraAPIUrl}{type}?token={self.token}"
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        answer = requests.post(url, data=json.dumps(data), headers=headers)
        return answer.json()

    def send_message(self, chatID, text):
        data = {"to": chatID,
                "body": text}
        answer = self.send_requests('messages/chat', data)
        return answer

    def send_image(self, chatID, imageURL):
        if not imageURL:
            imageURL = 'https://dickatyourdoor.com/cdn/shop/products/blank-box-chocolate-dick-991426_800x.jpg?v=1654026119'
        data = {"to": chatID,
                "image": imageURL}
        answer = self.send_requests('messages/image', data)
        return answer

    def send_document(self, chatID, document):
        data = {"to": chatID,
                "image": document}
        answer = self.send_requests('messages/document', data)
        return answer

    def incoming_msg(self):
        if self.dict_messages != []:
            message = self.dict_messages
            text = message['body'].split()
            if not message['fromMe']:
                chatID = message['from']
                if text[0].lower() == 'image':
                    return self.send_image(chatID, None)
            else:
                return 'NoCommand'
