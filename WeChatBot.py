import logging
import os
import time

from wxpy import *

bot = Bot()

# 打印来自其他好友、群聊和公众号的消息
@bot.register()
def print_others(msg):
    print(msg)

my_friend = bot.friends().search('青鸟', sex=FEMALE, city="宁波")[0]


# 回复 my_friend 的消息 (优先匹配后注册的函数!)
@bot.register(my_friend)
def reply_my_friend(msg):
    return 'received: {} ({})'.format(msg.text, msg.type)

# 自动接受新的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    if '我要入群' in msg.text.lower():
        # 接受好友请求
        new_friend = msg.card.accept()
        # 向新的好友发送消息
        new_friend.send('Hello，接下来将邀您入群。')
        # my_group = bot.groups().search('ㄧ道去台灣粉絲群1️')[0]
        my_group = bot.groups().search('测试1️')[0]
        my_group.add_members(new_friend)

 # 进入 Python 命令行、让程序保持运行
# embed()
bot.join()
