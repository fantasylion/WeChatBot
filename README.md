# WeChatBot
此项目基于[wxpy](http://wxpy.readthedocs.io)构建，自动添加好友，自动要求入群


### How to use

wxpy 支持 Python 3.4-3.6，以及 2.7 版本

```SHELL
pip install -U wxpy -i "https://pypi.doubanio.com/simple/"
```

### How to build to exe

```SHELL

pip install pyinstaller

pyinstaller -F fileName.py

# 如果不需要命令窗口用这个
pyinstaller -F -w fileName.py
```
[Build to exe](http://blog.csdn.net/mrlevo520/article/details/51840217)


