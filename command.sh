#!/bin/bash
playwright install --with-deps chromium 2>&1 | tail -2
python3 << 'PYEOF'
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=["--no-sandbox"])
    pg = b.new_context(viewport={"width":1280,"height":800}).new_page()
    pg.goto("https://openrouter.ai/sign-up", wait_until="domcontentloaded", timeout=30000)
    pg.wait_for_timeout(5000)
    gh = pg.locator("a:has-text(\"GitHub\"), button:has-text(\"GitHub\")").first
    gh.click(timeout=10000)
    pg.wait_for_timeout(6000)
    if "github.com" in pg.url:
        pg.fill("#login_field", "xushilianzhuren")
        pg.fill("#password", "aa798718..")
        pg.click("button[type=submit], input[type=submit]")
        pg.wait_for_timeout(10000)
        auth = pg.locator("button:has-text(\"Authorize\")")
        if auth.count() > 0: auth.click(); pg.wait_for_timeout(5000)
    pg.goto("https://openrouter.ai/settings/keys", wait_until="domcontentloaded", timeout=20000)
    pg.wait_for_timeout(5000)
    ck = pg.locator("button:has-text(\"Create Key\")")
    if ck.count() > 0:
        ck.click(); pg.wait_for_timeout(3000)
        ni = pg.locator("input[name*=name]")
        if ni.count() > 0: ni.fill("byz")
        cf = pg.locator("button:has-text(\"Create\")")
        if cf.count() > 0: cf.click(); pg.wait_for_timeout(5000)
    ke = pg.locator("code, pre")
    key = ke.first.text_content() if ke.count() > 0 else "NOT_FOUND:" + pg.url[:60]
    with open("/tmp/or_key.txt","w") as f: f.write(key)
    b.close()
PYEOF
cat /tmp/or_key.txt
