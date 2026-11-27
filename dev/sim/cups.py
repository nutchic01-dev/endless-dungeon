from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; storeMeta(m); }"); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>{ newRun(true); S.phase='walk'; S.floor=120; S.gold=99999; window.step=()=>{ S.q={id:'cups',step:0,flag:null,next:0}; S.phase='event'; S.ev=QUESTS.cups.steps[0](S.q); S.ev.type='quest'; }; document.querySelector('[data-act=hub][data-k=adv]')&&document.querySelector('[data-act=hub][data-k=adv]').click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=advback]')||document.querySelector('.hubhead [data-act=hub]'); b&&b.click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=walk]'); b&&b.click(); }"); time.sleep(.5)
    pg.screenshot(path='/tmp/cu0.png')
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=choose][data-i=\"0\"]'); b&&b.click(); }"); time.sleep(0.6); pg.screenshot(path='/tmp/cu1.png')
    time.sleep(1.6); pg.screenshot(path='/tmp/cu2.png')
    info=pg.evaluate("()=>S.ev&&S.ev.cups?[S.ev.cups.ball,S.ev.cups.T]:null"); print('info',info)
    time.sleep(info[1]); pg.screenshot(path='/tmp/cu3.png')
    pg.evaluate("(c)=>document.querySelector('.cupw[data-i=\"'+c+'\"]').click()", info[0]); time.sleep(.5); pg.screenshot(path='/tmp/cu4.png')
    print(pg.evaluate("()=>[S.gold, S.q&&S.q.flag, S.result&&S.result.text]")); print(errs[:3]); b.close()
