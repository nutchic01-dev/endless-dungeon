from playwright.sync_api import sync_playwright
import time,re,sys
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
sts=[int(a) for a in sys.argv[1:]] or [1,4,7]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for st in sts:
        for i in range(3):
            pg.evaluate(f"()=>{{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={{home:1}}; m.login={{last:dayKey(),streak:1}}; m.idle.st={st}; m.idle.sub=3; m.idle.best=Math.max(m.idle.best||0,60); storeMeta(m); }}"); time.sleep(.8)
            pg.goto(f'file:///home/claude/game/index.html?s{st}{i}'); time.sleep(2.5)
            if pg.evaluate("()=>loadMeta().idle.st")==st: break
        time.sleep(5); pg.screenshot(path=f'/tmp/wx_{st}.png')
    print(errs[:3]); b.close()
