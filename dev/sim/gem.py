from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; m.gem=300; m.chars.leo={star:3,form:false,recs:[],main:0}; storeMeta(m); }"); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>document.querySelector('[data-act=hub][data-k=shop]').click()"); time.sleep(.6)
    pg.screenshot(path='/tmp/gs1.png')
    r=pg.evaluate("""()=>{ const out=[]; for (let i=0;i<6;i++){ const bb=document.querySelector('[data-act=gsbuy][data-i="'+i+'"]'); if (bb) bb.click(); out.push(document.querySelector('.hubmsg')?document.querySelector('.hubmsg').textContent:''); } const m=loadMeta(); return [out, m.gem, m.sktix, m.tickets, m.gemDay]; }""")
    print(r)
    pg.evaluate("()=>{ const bb=document.querySelector('[data-act=gsrr]'); bb&&bb.click(); }"); time.sleep(.4); print('after rr', pg.evaluate("()=>[loadMeta().gem, document.querySelectorAll('[data-act=gsbuy]').length]"))
    pg.screenshot(path='/tmp/gs2.png')
    # energy buy
    pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const bb=document.querySelector('[data-act=htenbuy]'); bb&&bb.click(); }"); time.sleep(.4)
    print('energy', pg.evaluate("()=>{ const m=loadMeta(); return [m.ht.en, m.gem, m.gemDay.en, document.querySelector('.hubmsg')&&document.querySelector('.hubmsg').textContent]; }"))
    pg.screenshot(path='/tmp/gs3.png')
    print(errs[:3]); b.close()
