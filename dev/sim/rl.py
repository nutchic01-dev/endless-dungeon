from playwright.sync_api import sync_playwright
import time,re
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':760}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate("()=>{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={home:1,chars:1,bag:1}; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611','gift_d3_2811'],dyn:[]}; m.chars.leo={star:1,form:false,recs:[],main:0}; m.relics=[]; const ids=Object.keys(ALLCHARS); for (let k=0;k<60;k++) m.relics.push({uid:'r'+k,id:ids[k%ids.length],t:k%4,lv:0,subs:[]}); storeMeta(m); }"); time.sleep(.8)
        pg.goto(f'file:///home/claude/game/index.html?r{i}'); time.sleep(2.5)
        if pg.evaluate("()=>loadMeta().relics.length")==60: break
    pg.click('.hubnav [data-k=bag]'); time.sleep(.5); pg.click('[data-act=bagtab][data-k=relic]'); time.sleep(.5)
    def sc(): return pg.evaluate("()=>[...document.querySelectorAll('*')].filter(e=>e.scrollTop>0).map(e=>e.className+':'+e.scrollTop)")
    pg.mouse.move(195,500); pg.mouse.wheel(0,900); time.sleep(.5); print('bag before',sc())
    pg.evaluate("()=>{ const L=[...document.querySelectorAll('[data-act=rlsel]')]; const vis=L.find(e=>{const r=e.getBoundingClientRect(); return r.top>300&&r.top<600}); vis.click(); }"); time.sleep(.5); print('bag after',sc())
    pg.screenshot(path='/tmp/rl_bag.png')
    pg.click('.rlsx'); time.sleep(.3); print('closed', sc(), bool(pg.query_selector('.rlsheet')))
    pg.evaluate("()=>{ const b=document.createElement('button'); b.dataset.act='bagchar'; b.dataset.k='leo'; document.querySelector('.overlay').appendChild(b); b.click(); }"); time.sleep(.6)
    pg.click('[data-act=ctab][data-k=relic]'); time.sleep(.6)
    pg.evaluate("()=>{ const p=document.querySelector('.cpop'); if (p) p.scrollTop=600; }"); time.sleep(.3); print('hero before', sc())
    pg.evaluate("()=>{ const L=[...document.querySelectorAll('.cpop [data-act=rlsel]')]; const vis=L.find(e=>{const r=e.getBoundingClientRect(); return r.top>60&&r.top<400}); vis&&vis.click(); }"); time.sleep(.5); print('hero after', sc())
    pg.screenshot(path='/tmp/rl_hero.png')
    print(errs[:3]); b.close()
