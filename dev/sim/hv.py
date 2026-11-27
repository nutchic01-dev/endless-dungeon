from playwright.sync_api import sync_playwright
import time
INIT="localStorage.setItem('dq_guest','1');document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#dqload{display:none!important}#tut{display:none!important}';document.head.appendChild(s)});"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); pg=ctx.new_page(); pg.add_init_script(INIT); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611']}; ['leo','luna','mira','kira','toby','sage'].forEach(id=>m.chars[id]={star:3,form:id==='leo',recs:[],main:0}); m.ht={best:5,team:['leo',null,'luna',null,null]}; m.chars.leo.recs=[{power:9800,lv:100,floor:312,boss:300,date:1,el:'fire',st:{maxhp:42000,atk:5200,matk:900,def:3100,mdef:2400,cri:38,cridmg:220,pen:12,spd:110,type:'phy'},gear:{w:{name:'ดาบเพลิงนิรันดร์',r:4,plus:7,slot:'w'},a:{name:'เกราะมังกร',r:3,plus:5,slot:'a'}},skills:[]}]; m.relics=[{id:'leo',t:3,lv:5,subs:[{k:'cri',v:6},{k:'spd',v:4}],on:'leo'}]; m.eq=m.eq||{items:{},on:{},fl:1,fx:0,tix:30}; storeMeta(m); }"); time.sleep(3)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); }"); time.sleep(0.4)
    pg.evaluate("()=>document.querySelector('[data-act=htopen]').click()"); time.sleep(0.6)
    pg.evaluate("()=>document.querySelector('[data-act=htslot][data-i=\"1\"]').click()"); time.sleep(0.4)
    pg.evaluate("()=>document.querySelector('[data-act=hvsel][data-k=leo]').click()"); time.sleep(0.5)
    pg.screenshot(path='/tmp/hv1.png')
    pg.evaluate("()=>document.querySelector('.hvpop [data-act=htset]').click()"); time.sleep(0.4)
    print(pg.evaluate("()=>[JSON.stringify(loadMeta().ht.team), !!document.querySelector('.hvpop')]"))
    pg.evaluate("()=>document.querySelector('[data-act=htslot][data-i=\"3\"]').click()"); time.sleep(0.4)
    pg.evaluate("()=>document.querySelector('[data-act=hvsel][data-h=\"1\"]').click()"); time.sleep(0.5)
    pg.screenshot(path='/tmp/hv2.png')
    print(errs); b.close()
