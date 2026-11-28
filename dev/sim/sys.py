from playwright.sync_api import sync_playwright
import time,re
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.add_init_script("Date.prototype.getHours=function(){return 14;}")
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate("()=>{ const m=loadMeta(); m.name='ผู้กล้านอนน้อย'; m.tut={home:1}; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611','gift_d3_2811'],dyn:[]}; m.idle.st=4; m.idle.sub=4; m.idle.best=90; m.idle.farm=true; ['leo','lumina','nyx','sage','raven','mira'].forEach(id=>{ m.chars[id]={star:3,form:false,recs:[],main:0}; }); m.spirit={own:{phoenix:{lv:6,st:1,cp:0}},eq:{ht:null,dh:null,city:'phoenix'},ess:20,nest:{day:dayKey(),left:2,best:0},eggs:[0,1,0]}; m.idle.hero=Object.assign(m.idle.hero||{},{tank:'leo',support:'lumina',mage:'sage',warrior:'nyx',archer:'raven',assassin:'mira'}); storeMeta(m); }"); time.sleep(.8)
        pg.goto(f'file:///home/claude/game/index.html?y{i}'); time.sleep(3)
        if pg.evaluate("()=>loadMeta().name")=='ผู้กล้านอนน้อย': break
    time.sleep(4); pg.screenshot(path='/tmp/sys_home.png')
    pg.click('[data-act=syso]'); time.sleep(.5); pg.screenshot(path='/tmp/sys_pop.png')
    pg.evaluate("()=>document.querySelector('.syspop').scrollTop=600"); time.sleep(.3); pg.screenshot(path='/tmp/sys_pop2.png')
    pg.click('.sysi[data-a=nestopen]'); time.sleep(.8); print('after go:', pg.evaluate("()=>(document.querySelector('.hubhead')||{}).innerText"))
    print(errs[:3]); b.close()
