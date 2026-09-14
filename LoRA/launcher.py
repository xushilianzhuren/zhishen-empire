# 分离启动器v3·破缓存下载·2026-09-14
import subprocess, urllib.request, time
url = "https://gh-proxy.com/https://raw.githubusercontent.com/xushilianzhuren/zhishen-empire/main/LoRA/train_stage1.py?t=" + str(int(time.time()))
urllib.request.urlretrieve(url, "/home/aistudio/train_stage1.py")
print("SCRIPT_DOWNLOADED", len(open("/home/aistudio/train_stage1.py").read()))
subprocess.Popen(["python","/home/aistudio/train_stage1.py"],
    stdout=open("/home/aistudio/train_stage1.log","w"),
    stderr=subprocess.STDOUT, start_new_session=True)
print("TRAIN_LAUNCHED")
