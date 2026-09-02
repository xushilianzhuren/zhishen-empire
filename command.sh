#!/bin/bash
echo "=== 网络探测 ==="
for url in "https://openrouter.ai/api/v1/models" "https://api.groq.com/openai/v1/models" "https://api.mistral.ai/v1/models"; do
  code=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 -m 8 "$url" 2>/dev/null)
  echo "$(echo $url | cut -d/ -f3) $code"
done
echo "=== OpenRouter免费模型 ==="
curl -s "https://openrouter.ai/api/v1/models" | python3 -c "
import json,sys
d=json.load(sys.stdin)
free=[m for m in d.get('data',[]) if ':free' in m.get('id','')]
print(f'free: {len(free)}')
for m in free:
    print(m['id'])
" 2>&1
echo "=== pip ==="
pip install openai 2>&1 | tail -1
