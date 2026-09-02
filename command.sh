#!/bin/bash
echo "=== 安装playwright ==="
pip install playwright 2>&1 | tail -1
playwright install chromium 2>&1 | tail -1
echo "=== 安装完成，启动注册脚本 ==="
python3 << 'PYEOF'
from playwright.sync_api import sync_playwright
import json, time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={'width':1280,'height':800})
    page = ctx.new_page()
    
    # GitHub OAuth登录OpenRouter
    page.goto('https://openrouter.ai/sign-up', wait_until='domcontentloaded', timeout=30000)
    page.wait_for_timeout(5000)
    
    # 点Sign in with GitHub
    gh = page.locator('a:has-text("GitHub"), button:has-text("GitHub")').first
    gh.click(timeout=10000)
    page.wait_for_timeout(5000)
    
    # GitHub授权页
    if 'github.com' in page.url:
        # 填GitHub凭据
        page.fill('#login_field', 'xushilianzhuren')
        page.fill('#password', 'aa798718..')
        page.click('input[type=submit], button[type=submit]')
        page.wait_for_timeout(8000)
        # 可能需要授权
        auth = page.locator('button:has-text("Authorize")')
        if auth.count() > 0:
            auth.click()
            page.wait_for_timeout(5000)
    
    # 登录后去Keys页面
    page.goto('https://openrouter.ai/settings/keys', wait_until='domcontentloaded', timeout=20000)
    page.wait_for_timeout(5000)
    
    # 创建API Key
    create = page.locator('button:has-text("Create Key")')
    if create.count() > 0:
        create.click()
        page.wait_for_timeout(3000)
        # 填Key名字
        name_input = page.locator('input[name*=name], input[placeholder*=name]')
        if name_input.count() > 0:
            name_input.fill('baiyouzhen')
        page.wait_for_timeout(1000)
        # 确认创建
        confirm = page.locator('button:has-text("Create")')
        if confirm.count() > 0:
            confirm.click()
            page.wait_for_timeout(5000)
    
    # 读取Key
    key_el = page.locator('code, pre, [class*=key]')
    if key_el.count() > 0:
        api_key = key_el.first.text_content()
        print(f'API_KEY:{api_key}')
    else:
        print('KEY_NOT_FOUND')
        print(f'当前URL: {page.url}')
    
    browser.close()
PYEOF
