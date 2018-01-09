#!/usr/bin/env python
# -*- coding:utf-8 -*-

import tkinter as tk
from tkinter import messagebox
import threading
from time import ctime, sleep
from wxpy import *


def closeProcess(*e):
    """
    Kill the process
    """
    window.destroy()
    sys.exit(0)


window = tk.Tk()
window.title('WeChatBot')
window.geometry('450x600')
window.protocol("WM_DELETE_WINDOW", closeProcess)

alreadyDraw = False
alreadyLogin = False
bot = None


def writeQR(picDir, qrStorage):
    with open(picDir, 'wb') as f:
        f.write(qrStorage)


def drawWechatWindow(qrcodes):
    print("drawWechatWindow......")
    global alreadyLogin
    while not alreadyLogin:
        picDir = 'D:/DATA/code/WeChatBot/images/test.png'

        writeQR(picDir, qrcodes)
        image_file = tk.PhotoImage(file=picDir)
        tk.Label(window, image=image_file).place(x=0, y=0)

        tk.Label(window, text="Scan the QR code.").place(x=165, y=460)
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

lb = None
varLable= None
openAutoJoinGroups = False
comment = None

def drawGroups():
    global bot
    global lb
    global varLable
    global comment

    lb = tk.Listbox(window)
    lb.place(x=0, y=0)
    for group in bot.groups():
        try:
            lb.insert('end', group.name)
        except Exception:
            lb.insert('end', 'Unknow')
    lb.pack()

    varLable = tk.StringVar()  # 创建变量
    varLable.set("Plase choose one option.")
    l = tk.Label(window, bg='yellow', width=50, textvariable=varLable)
    l.pack()

    b1 = tk.Button(window, text='print selection', width=15,
                   height=2, command=comfirm)
    b1.place(x=0, y=100)
    b1.pack()

    comment = tk.StringVar()  # 定义变量
    comment.set('Please input comment')  # 变量赋值
    inputCommentBox = tk.Entry(window, textvariable=comment)
    inputCommentBox.place(x=0,y=150)
    inputCommentBox.pack()


def comfirm():
    """
    Comfirm the lable choose
    :return:
    """
    global lb
    global varLable
    global openAutoJoinGroups

    try:
        varle = lb.get(lb.curselection())
        varLable.set(varle)
        openAutoJoinGroups = True
        my_group = bot.groups().search(varLable.get())[0]
        print(varle)
    except Exception:
        tk.messagebox.showinfo(title='Warning', message='Please choose one group! ')
        return




def weChatBot(wcache_path, wconsole_qr, wqr_path, wqr_callback, wlogin_callback, wlogout_callback):
    global bot
    bot = Bot(cache_path=None, console_qr=False, qr_path=None, qr_callback=qrWindow, login_callback=loginSuccess,
              logout_callback=None)
    drawGroups()

    # 自动接受新的好友请求
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(msg):
        global varLable
        global openAutoJoinGroups
        global comment

        # Not open the auto Join groups
        if not openAutoJoinGroups:
            return

        if comment.get() in msg.text.lower():
            # 接受好友请求
            new_friend = msg.card.accept()
            # 向新的好友发送消息
            new_friend.send('你知道')
            new_friend.send(varLable.get())
            new_friend.send('吗')
            # my_group = bot.groups().search(varLable.get())[0]
            # my_group.add_members(new_friend)


startThread(weChatBot, (None, False, None, qrWindow, loginSuccess, None))

window.mainloop()
