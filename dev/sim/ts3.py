from playwright.sync_api import sync_playwright
import time, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("""()=>{ SND.set.voice=0; SND.set.sfx=0; SND.set.mus=0; const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611']}; m.chars={};
      const gear={a:{name:'ดาบผู้กล้า',r:3,plus:6,set:'brave',slot:'weapon'},b:{name:'หมวกผู้กล้า',r:3,plus:5,set:'brave',slot:'helm'},c:{name:'ขนนกฟีนิกซ์',r:3,plus:4,acc:'feather',slot:'acc'},d:{name:'ผ้าคลุม',r:2,plus:3,acc:'cloak',slot:'acc2'}};
      ['leo','luna','mira','serena','seris'].forEach(id=>m.chars[id]={star:4,form:false,main:0,recs:[{power:3000,lv:100,floor:300,boss:300,st:{maxhp:9000,atk:1500,matk:1500,def:900,mdef:800,cri:20,cridmg:200,pen:8,spd:110,type:'phy'},gear,skills:[{name:'x',lv:3}],passives:['vital']}]});
      m.ht={best:44,team:['leo','mira','serena','luna','seris']}; m.ht.en=60; storeMeta(m); }"""); time.sleep(2)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("""()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click(); window.__ht.htStart(45); const F=window.__ht.F(); clearInterval(F.iv); let n=0; while(!F.done&&n<6000){ window.__ht.htTick(); n++; } }"""); time.sleep(1)
    print(pg.evaluate("()=>{ const F=window.__ht.F(); return [F.win, F.T.map(h=>[h.id,Math.round(h.dd),Math.round(h.tk),Math.round(h.hl),h.rv,h.hp>0])]; }"))
    pg.screenshot(path='/tmp/ts0.png'); pg.evaluate("()=>document.querySelector('[data-act=tsum]').click()"); time.sleep(.6); pg.screenshot(path='/tmp/ts0b.png'); pg.query_selector('.tspop').screenshot(path='/tmp/ts1.png'); pg.query_selector('.tspop').screenshot(path='/tmp/ts1.png')
    pg.evaluate("()=>{ document.querySelector('[data-act=tsumc]').click(); document.querySelector('[data-act=htclose]').click(); }"); time.sleep(.5)
    pg.evaluate("()=>{ const b=document.querySelector('.hubhead [data-act=hub]'); b&&b.click(); }"); time.sleep(.3)
    pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=dhopen]').click(); }"); time.sleep(.6); 
    for hid in ['mira','luna','seris']:
        pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhpick]'); b&&b.click(); }"); time.sleep(.3)
        pg.evaluate("(k)=>{ const b=document.querySelector('[data-act=hvsel][data-k='+k+']'); b&&b.click(); }", hid); time.sleep(.3)
        pg.evaluate("()=>{ const b=document.querySelector('.pop [data-act=dhtog]'); b&&b.click(); }"); time.sleep(.3)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhpickc]'); b&&b.click(); }"); time.sleep(.3)
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhstart]'); b&&b.click(); }"); time.sleep(6); pg.screenshot(path='/tmp/dh1.png'); pg.evaluate("()=>document.querySelector('[data-act=dhskip]').click()"); time.sleep(1.5); pg.screenshot(path='/tmp/dh3.png'); pg.evaluate("()=>{ const b=document.querySelector('[data-act=tsum]'); b&&b.click(); }"); time.sleep(.6); e=pg.query_selector('.tspop'); e and e.screenshot(path='/tmp/dh2.png')
    print('dragon', pg.evaluate("()=>document.getElementById('dhdmg')&&document.getElementById('dhdmg').textContent"))
    print(errs[:3]); b.close()
