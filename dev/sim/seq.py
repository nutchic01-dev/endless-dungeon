from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; storeMeta(m); }"); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>{ newRun(true); S.phase='walk'; S.floor=120; S.gold=99999; window.step=()=>{ S.phase='event'; S.ev=seqEv('route','ประตูอักขระเวท','🚪','ประตูหินสลักอักขระสามแบบ อักขระจะสว่างขึ้นเป็นลำดับ ต้องกดซ้ำให้ถูกลำดับประตูจึงจะเปิด',(r,ans)=>done(r+' | '+ans,'good'),()=>done('skip')); }; document.querySelector('[data-act=hub][data-k=adv]')&&document.querySelector('[data-act=hub][data-k=adv]').click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=advback]')||document.querySelector('.hubhead [data-act=hub]'); b&&b.click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=walk]'); b&&b.click(); }"); time.sleep(.5)
    pg.screenshot(path='/tmp/cu0.png')
    time.sleep(1.2); pg.screenshot(path='/tmp/sq1.png')
    info=pg.evaluate("()=>[S.ev.seq.s, S.ev.seq.T]"); print('info',info)
    time.sleep(info[1]); pg.screenshot(path='/tmp/sq2.png')
    for k,r in enumerate(info[0]):
        pg.evaluate("(r)=>document.querySelector('.seqr[data-i=\"'+r+'\"]').click()", r); time.sleep(.25)
        if k==1: pg.screenshot(path='/tmp/sq3.png')
    print(pg.evaluate("()=>[S.result&&S.result.text, S.phase]")); print(errs[:3]); b.close()
