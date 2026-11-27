from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
REC="{power:%d,lv:%d,floor:%d,boss:%d,date:1,el:'light',st:{maxhp:%d,atk:%d,matk:200,def:%d,mdef:%d,cri:%d,cridmg:%d,pen:%d,spd:%d,type:'phy'},gear:{weapon:{name:'ดาบเพลิง',r:%d,plus:%d,set:'s1',slot:'weapon',icon:'⚔️'},armor:{name:'เกราะมังกร',r:2,plus:4,set:'s1',slot:'armor',icon:'🥋'}},skills:[{name:'โล่ราชสีห์',lv:%d},{name:'คำรามสิงห์',lv:3}],passives:['vital']}"
OLD=REC%(2400,90,260,250,8200,1300,900,700,18,190,8,105,2,5,3)
NEW=REC%(3100,100,330,320,9800,1650,1000,760,21,205,11,112,3,8,4)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.chars.leo={star:3,form:false,recs:[%s],main:0,pend:%s}; storeMeta(m); }"%(OLD,NEW)); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=chars]').click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ [...document.querySelectorAll('[data-act=cpop]')].find(x=>x.dataset.k==='leo').click(); }"); time.sleep(.6)
    pg.screenshot(path='/tmp/rc0.png'); print(pg.evaluate("()=>[!!loadMeta().chars.leo.pend, document.querySelectorAll('[data-act=cpop]').length, !!document.querySelector('.pop')]"))
    el=pg.query_selector('.reccmp'); el.scroll_into_view_if_needed(); el.screenshot(path='/tmp/rc1.png')
    pg.click('[data-act=recask][data-v=new]'); time.sleep(.4); pg.screenshot(path='/tmp/rc2.png')
    pg.click('[data-act=recok]'); time.sleep(.6)
    print(pg.evaluate("()=>{ const c=loadMeta().chars.leo; return [c.recs.length, c.recs[0].power, !!c.pend]; }"))
    # victory flow
    print(pg.evaluate("""()=>{ newRun(true); pickClass('tank'); S.pendingParty=false; S.pendingChar=false; S.pendingAwaken=false; S.reveal=null; S.char=ALLCHARS.leo.c; S.floor=400; S.lv=100; endRun(true,'boss'); return [!!loadMeta().chars.leo.pend, S.phase]; }"""))
    pg.evaluate("""()=>{ const b=document.querySelector('.hubhead [data-act=hub]'); if (b) b.click(); }"""); time.sleep(.7)
    pg.screenshot(path='/tmp/rc4.png'); el=pg.query_selector('.reccmp'); print('cmp', bool(el))
    if el:
        el.scroll_into_view_if_needed(); el.screenshot(path='/tmp/rc3.png')
        pg.click('.reccmp [data-act=recask][data-v=old]'); time.sleep(.3); pg.click('[data-act=recok]'); time.sleep(.5)
        print(pg.evaluate("""()=>{ const c=loadMeta().chars.leo; const n=document.querySelector('.recnote'); return [c.recs.length,c.recs[0].power,!!c.pend, n&&n.textContent]; }"""))
    print(errs[:3])
    b.close()
