from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; storeMeta(m); }"); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=guideopen]'); if (b) b.click(); else { const s=document.querySelector('[data-act=settings]'); s&&s.click(); } }"); time.sleep(.4)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=guideopen]'); b&&b.click(); }"); time.sleep(.5)
    pg.screenshot(path='/tmp/gd1.png', full_page=True)
    for k in ['rec','res','time']:
        pg.evaluate("(k)=>{ const b=document.querySelector('[data-act=gdtab][data-k='+k+']'); b&&b.click(); }",k); time.sleep(.4); pg.screenshot(path=f'/tmp/gd_{k}.png', full_page=True)
    # in-run help
    pg.evaluate("()=>{ newRun(true); S.phase='walk'; window.step=()=>{}; const b=document.querySelector('.hubhead [data-act=hub]'); b&&b.click(); }"); time.sleep(.4)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=hub][data-k=adv]'); b&&b.click(); const c=document.querySelector('[data-act=advback]'); c&&c.click(); }"); time.sleep(.4)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=walk]'); b&&b.click(); }"); time.sleep(.4)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=rhelp]'); b&&b.click(); }"); time.sleep(.5); pg.screenshot(path='/tmp/gd_run.png')
    print(errs[:3]); b.close()
