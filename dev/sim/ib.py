from playwright.sync_api import sync_playwright
import time,re
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    print(pg.evaluate("()=>BANDS.length"))
    for sub,tag in [(5,'m'),(10,'b')]:
        for i in range(3):
            pg.evaluate(f"()=>{{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={{home:1}}; m.login={{last:dayKey(),streak:1}}; m.idle.st=4; m.idle.sub={sub}; storeMeta(m); }}"); time.sleep(.8)
            pg.goto(f'file:///home/claude/game/index.html?{tag}{i}'); time.sleep(2.5)
            if pg.evaluate("()=>loadMeta().idle.sub")=={sub}: break
        time.sleep(9); pg.screenshot(path=f'/tmp/ib_{tag}.png')
    pg.evaluate("()=>{ newRun(true); S.phase='walk'; }")
    print(errs[:3]); b.close()
