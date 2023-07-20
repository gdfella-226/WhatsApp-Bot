from tools.BotHandler import ultraChatBot
from tools.convert import convert


def home():
    convert()
    # bot = ultraChatBot()
    # res = bot.listen()
    # output = open('./msgs.json', 'w')
    # output.write(res)


if __name__ == '__main__':
    home()
