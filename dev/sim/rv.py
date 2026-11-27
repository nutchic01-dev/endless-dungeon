from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("""()=>{ SND.set.voice=0; SND.set.sfx=0; SND.set.mus=0; const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611']}; m.chars={};
      const gear={a:{name:'ดาบผู้กล้า',r:3,plus:6,set:'brave',slot:'weapon'},b:{name:'หมวกผู้กล้า',r:3,plus:5,set:'brave',slot:'helm'},c:{name:'ขนนกฟีนิกซ์',r:3,plus:4,acc:'feather',slot:'acc'},d:{name:'ผ้าคลุม',r:2,plus:3,acc:'cloak',slot:'acc2'}};
      ['leo','luna','mira','lumina','seris'].forEach(id=>m.chars[id]={star:4,form:false,main:0,recs:[]});
      m.ht={best:60,team:['leo','mira','lumina','luna','seris']}; m.ht.en=60; storeMeta(m); }"""); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("""()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click(); window.__ht.htStart(33); const F=window.__ht.F(); clearInterval(F.iv); let n=0; while(!F.done&&n<6000){ window.__ht.htTick(); n++; } }"""); time.sleep(1)
    print(pg.evaluate("()=>{ const F=window.__ht.F(); return [F.win, F.T.map(h=>[h.id,h.uc||0,h.rvd||0,h.rvU||0,h.hp>0])]; }"))
    pg.query_selector('.htres').screenshot(path='/tmp/ts0.png'); pg.evaluate("()=>document.querySelector('[data-act=tsum]').click()"); time.sleep(.6); pg.screenshot(path='/tmp/ts0b.png'); pg.query_selector('.tspop').screenshot(path='/tmp/ts1.png'); pg.query_selector('.tspop').screenshot(path='/tmp/ts1.png')
    print(errs[:3]); b.close()
