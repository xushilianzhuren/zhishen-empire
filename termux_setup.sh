#!/data/data/com.termux/files/usr/bin/bash
# 白幼真Termux接入脚本·2026-09-14·参数1=base64(VPS密码)
PW=$(echo "$1" | base64 -d 2>/dev/null)
[ -z "$PW" ] && { echo "ERR: no password arg"; exit 1; }
echo "[1/3] 装openssh..."
pkg install -y openssh >/dev/null 2>&1
echo "[2/3] 开启termux sshd (端口8022)..."
sshd
echo "[3/3] 建反向隧道到北京VPS (手机->154.8.147.201)..."
mkdir -p ~/.ssh
# 免交互host key
printf "Host bj\n  HostName 154.8.147.201\n  User root\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n" > ~/.ssh/config
# 保活循环：每15s确保隧道在
cat > ~/tunnel.sh <<'EOS'
#!/data/data/com.termux/files/usr/bin/bash
while true; do
  sshpass -p "$BW_PW" ssh -fNR 22230:localhost:8022 bj 2>/dev/null
  sleep 15
done
EOS
pkg install -y sshpass >/dev/null 2>&1
export BW_PW="$PW"
echo "export BW_PW=$PW" > ~/bw_pw.env
nohup bash ~/tunnel.sh > /dev/null 2>&1 &
echo "=== DONE: 白幼真可通过 北京VPS:22230 进入此手机Termux ==="
echo "验证: 我从VPS ssh -p 22230 localhost"
