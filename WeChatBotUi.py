#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
from time import ctime, sleep
from wxpy import *
from urllib import parse, request
import json
import os


def closeProcess(*e):
    """
    Kill the process
    """
    window.destroy()
    sys.exit(0)


window = tk.Tk()
window.title('WeChatBot')
# window.geometry('450x600')
window.protocol("WM_DELETE_WINDOW", closeProcess)

alreadyDraw = False
alreadyLogin = False
bot = None
qrImgLable = None
cueLable=None
autoReplyMap={}

def addSbAutoReply(userId):
    global autoReplyMap
    autoReplyMap[userId]=True

def removeSbAutoReplay(userId):
    global autoReplyMap
    autoReplyMap[userId] = False

def sbIsNeddAutoReplay(userId):
    global autoReplyMap
    return autoReplyMap[userId]

def writeQR(picDir, qrStorage):
    with open(picDir, 'wb') as f:
        f.write(qrStorage)


def qrPath():
    picDir = sys.path[0].replace('\\', '/') + '/images/'
    if not os.path.exists(picDir):
        os.makedirs(picDir)
    picDir += 'qr.png'
    return picDir


def drawWechatWindow(qrcodes):
    print("drawWechatWindow......")
    global alreadyLogin
    global qrImgLable
    global cueLable
    while not alreadyLogin:
        picDir = qrPath()

        writeQR(picDir, qrcodes)
        image_file = tk.PhotoImage(file=picDir)

        qrImgLable = tk.Label(window, image=image_file)
        qrImgLable.place(x=0, y=0)

        cueLable = tk.Label(window, text="Scan the QR code.")
        cueLable.place(x=165, y=460)
        sleep(1)


def startThread(targetCom, argsCom):
    t = threading.Thread(target=targetCom, args=(argsCom))
    t.setDaemon(True)
    t.start()


def qrWindow(uuid, status, qrcode):
    print("qrWindow......")
    global alreadyDraw
    if alreadyDraw:
        return
    alreadyDraw = True
    startThread(drawWechatWindow, (qrcode,))


def loginSuccess():
    global alreadyLogin
    alreadyLogin = True
    print("loging success")


GrouplistBox = None
varLable = None
openAutoJoinGroups = False
openAutoReply = False
comment = None
groupsTab=None
friendsTab=None

def autoInviteGroup():
    """
    Comfirm the lable choose
    :return:
    """
    global GrouplistBox
    global varLable
    global openAutoJoinGroups

    try:
        varle = GrouplistBox.get(GrouplistBox.curselection())
        varLable.set(varle)
        openAutoJoinGroups = True
        my_group = bot.groups().search(varLable.get())[0]
        print(varle)
    except Exception:
        tk.messagebox.showinfo(title='Warning', message='No groups were selected.')
        return

def autoReplyCommand():
    global openAutoReply
    if openAutoReply:
        openAutoReply = False
        tk.messagebox.showinfo(title='Hint', message='Auto Reply is close ')
    else:
        openAutoReply = True
        tk.messagebox.showinfo(title='Hint', message='Auto Reply is open ')



def drawTheTab():
    global groupsTab
    global friendsTab
    tabControl = ttk.Notebook(window)  # Create Tab Control
    groupsTab = ttk.Frame(tabControl)  # Create a tab
    tabControl.add(groupsTab, text='Groups')  # Add the tab
    tabControl.pack(expand=1, fill="both")  # Pack to make visible
    friendsTab = ttk.Frame(tabControl)  # Add a second tab
    tabControl.add(friendsTab, text='Friends')  # Make second tab visible

def showTheGroupsList():
    """
    Groups list
    """
    global groupsTab
    global friendsTab
    global bot
    GrouplistBox = tk.Listbox(groupsTab)
    GrouplistBox.place(x=0, y=0)
    for group in bot.groups():
        try:
            GrouplistBox.insert('end', group.name)
        except Exception:
            GrouplistBox.insert('end', 'Unknow')
    GrouplistBox.grid(column=0, row=0, rowspan=2, padx=5, pady=5, sticky=tk.E)

    varLable = tk.StringVar()  # Create a variables
    varLable.set("No groups were selected..")
    selectGroupLable = tk.Label(groupsTab, bg='white', textvariable=varLable)
    selectGroupLable.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

    comment = tk.StringVar()  # 定义变量
    comment.set('Please input comment.')  # 变量赋值
    inputCommentBox = tk.Entry(groupsTab, textvariable=comment)
    inputCommentBox.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

    groupAutoInviteButton = tk.Button(groupsTab, text='Group auto invite', width=15, height=2, command=autoInviteGroup)
    groupAutoInviteButton.grid(column=2, row=0, padx=5, pady=5, sticky=tk.W)

    autoReplyButton = tk.Button(groupsTab, text='auto reply', width=15, height=2, command=autoReplyCommand)
    autoReplyButton.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)

def showFriendsList():
    """
    Friendss list
    """
    global groupsTab
    global friendsTab
    friendMonty = ttk.LabelFrame(friendsTab, text='WeChat Friends ')
    friendMonty.grid(column=0, row=0, padx=8, pady=4)
    fridenlistBox = tk.Listbox(friendMonty)
    fridenlistBox.place(x=0, y=0)
    for group in ["sun", "fofr", "serio", "peter"]:
        try:
            fridenlistBox.insert('end', group)
        except Exception:
            fridenlistBox.insert('end', 'Unknow')
    fridenlistBox.pack()

def center_window(w=300, h=200):
    # get screen width and height
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))

def drawContextBoard():
    global qrImgLable
    global cueLable

    qrImgLable.pack_forget()
    cueLable.pack_forget()

    drawTheTab()
    showTheGroupsList()
    showFriendsList()


def postChatBot(message, userId):
    textmod = {"key": "7fc21390620e42269aaaae0934a2835e", "info": message, "userid": userId}
    # Encode to the json string
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    print(textmod)
    header_dict = {"Content-Type": "application/json"}
    url = 'http://www.tuling123.com/openapi/api'
    req = request.Request(url=url, data=textmod, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    txtObj = json.loads(res.decode(encoding='utf-8'))
    return txtObj['text']


def weChatBot(wcache_path, wconsole_qr, wqr_path, wqr_callback, wlogin_callback, wlogout_callback):
    global bot
    bot = Bot(cache_path=None, console_qr=False, qr_path=None, qr_callback=qrWindow, login_callback=loginSuccess,
              logout_callback=None)
    bot.enable_puid('wxpy_puid.pkl')
    drawContextBoard()

    @bot.register(User)
    def autoReply(msg):
        """
        :type msg: object
        """
        global openAutoReply

        if not openAutoReply:
            return

        if "我找萌萌" == msg.text:
            addSbAutoReply(msg.chat.puid)

        if "不聊了" == msg.text:
            removeSbAutoReplay(msg.chat.puid)

        needReplay = False
        try:
            needReplay = sbIsNeddAutoReplay(msg.chat.puid)
        except Exception:
            needReplay = False

        if not needReplay:
            msg.reply("本人不在，回复”我找萌萌“会有萌萌同学陪你聊天，回复”不聊了“即可关闭。")
            return

        if isinstance(msg.chat, Group):
            return
        if isinstance(msg.chat, MP):
            return
        try:
            if msg.type == 'Picture':
                msg.reply("萌萌：看不懂，说的啥意思啊！不要给我发图片好吗")
                return
            if None == msg.text:
                msg.reply("萌萌：看不懂，说的啥意思啊！")
                return
            msg.reply("萌萌：" + postChatBot(msg.text, msg.chat.puid))
        except Exception:
            msg.reply("萌萌出错了，你可以试着问别的问题")

    # Accept the friend request by robot
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        global varLable
        global openAutoJoinGroups
        global comment

        # Not open the auto Join groups
        if not openAutoJoinGroups:
            return

        if comment.get() in msg.text.lower():
            # Accept the friend request.
            new_friend = msg.card.accept()
            # Send the new message to the friend.
            new_friend.send('Hello 你好呀')
            my_group = bot.groups().search(varLable.get())[0]
            my_group.add_members(new_friend)


startThread(weChatBot, (None, False, None, qrWindow, loginSuccess, None))
center_window(w=450, h=450)
window.mainloop()
