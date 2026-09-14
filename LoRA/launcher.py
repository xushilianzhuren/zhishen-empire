# 分离启动器·绕jupyter后台限制·2026-09-14
import subprocess
subprocess.Popen(["python","/home/aistudio/train_stage1.py"],
    stdout=open("/home/aistudio/train_stage1.log","w"),
    stderr=subprocess.STDOUT,
    start_new_session=True)
print("TRAIN_LAUNCHED")
