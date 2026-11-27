from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1).replace('#tut{display:none!important}','')
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(3)
    for i in range(12):
        if pg.query_selector('#tutname'): break
        if not pg.query_selector('#tut') and pg.query_selector('.pop-bg .choice'): pg.click('.pop-bg .choice'); time.sleep(1); continue
        if pg.query_selector('[data-tut=next]'): pg.click('[data-tut=next]'); time.sleep(.4)
        else: time.sleep(1)
    pg.screenshot(path='/tmp/tn1.png')
    pg.fill('#tutname','a'); pg.click('[data-tut=next]'); time.sleep(.3); print(pg.inner_text('#tutnerr'))
    pg.fill('#tutname','ฟ้าใส'); pg.click('[data-tut=next]'); time.sleep(.5); print(pg.evaluate("()=>loadMeta().name"), bool(pg.query_selector('#tutname'))); pg.screenshot(path='/tmp/tn2.png')
    print(errs[:3]); b.close()
