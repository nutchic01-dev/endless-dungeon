from playwright.sync_api import sync_playwright
import time,re
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=3); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate("()=>{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={home:1}; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611','gift_d3_2811'],dyn:[]}; m.idle.st=6; m.idle.sub=2; storeMeta(m); }"); time.sleep(.8)
        pg.goto(f'file:///home/claude/game/index.html?w{i}'); time.sleep(3)
        if pg.evaluate("()=>loadMeta().name")=='ทดสอบ': break
    time.sleep(3)
    for f in range(24): pg.screenshot(path=f'/tmp/wf{f}.png', clip={'x':0,'y':400,'width':390,'height':110}); time.sleep(0.08)
    print(errs[:3]); b.close()
