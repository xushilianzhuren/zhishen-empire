# 分离启动器v4·2026-09-14
import subprocess, urllib.request
url = "https://gh-proxy.com/https://raw.githubusercontent.com/xushilianzhuren/zhishen-empire/main/LoRA/train_stage2.py"
urllib.request.urlretrieve(url, "/home/aistudio/train_stage2.py")
print("SCRIPT_DOWNLOADED", len(open("/home/aistudio/train_stage2.py").read()))
subprocess.Popen(["python","/home/aistudio/train_stage2.py"],
    stdout=open("/home/aistudio/train_stage2.log","w"),
    stderr=subprocess.STDOUT, start_new_session=True)
print("TRAIN_LAUNCHED")
