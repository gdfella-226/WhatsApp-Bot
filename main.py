from tools.BotHandler import ultraChatBot


def home():
    bot = ultraChatBot()
    res = bot.listen()
    #output = open('./msgs.json', 'w')
    #output.write(res)



if (__name__) == '__main__':
    home()
