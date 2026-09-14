# 分离启动器v2·自带下载训练脚本·2026-09-14
import subprocess, urllib.request
url="https://gh-proxy.com/https://raw.githubusercontent.com/xushilianzhuren/zhishen-empire/main/LoRA/train_stage1.py?t="+str(__import__("time").time())"
urllib.request.urlretrieve(url, "/home/aistudio/train_stage1.py?t="+str(__import__("time").time())")
print("SCRIPT_DOWNLOADED")
subprocess.Popen(["python","/home/aistudio/train_stage1.py?t="+str(__import__("time").time())"],
    stdout=open("/home/aistudio/train_stage1.log","w"),
    stderr=subprocess.STDOUT, start_new_session=True)
print("TRAIN_LAUNCHED")
