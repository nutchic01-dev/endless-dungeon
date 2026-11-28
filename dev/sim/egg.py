from playwright.sync_api import sync_playwright
import time,re
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate("()=>{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={home:1}; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; m.spirit={own:{daopui:{lv:1,st:1,cp:0}},eq:{ht:'daopui',dh:null,city:null},ess:20,nest:{day:'',left:3,best:0},eggs:[2,0,1]}; storeMeta(m); }"); time.sleep(.8)
        pg.goto(f'file:///home/claude/game/index.html?e{i}'); time.sleep(2.5)
        if pg.evaluate("()=>loadMeta().name")=='ทดสอบ': break
    # mail claim
    pg.evaluate("()=>{ const b=document.createElement('button'); b.dataset.act='mailopen'; document.querySelector('.overlay').appendChild(b); b.click(); }"); time.sleep(.6)
    if pg.query_selector('[data-act=mailget][data-k=gift_d3_2811]'):
        pg.screenshot(path='/tmp/egg_mail0.png'); pg.click('[data-act=mailget][data-k=gift_d3_2811]'); time.sleep(.5); pg.screenshot(path='/tmp/egg_mail.png')
    print('after mail', pg.evaluate("()=>{ const m=loadMeta(); return [m.sktix,m.rtix,m.spirit.eggs] }"))
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=mailclose]'); b&&b.click(); }"); time.sleep(.3)
    pg.click('.hubnav [data-k=bag]'); time.sleep(.6)
    pg.click('[data-act=bagitem][data-k=egg1]'); time.sleep(.4); pg.screenshot(path='/tmp/egg_bag.png')
    pg.click('[data-act=eggopen]'); time.sleep(.5); pg.screenshot(path='/tmp/egg_o1.png'); time.sleep(1.3); pg.screenshot(path='/tmp/egg_o2.png'); time.sleep(1); pg.screenshot(path='/tmp/egg_o3.png')
    print('after open', pg.evaluate("()=>{ const m=loadMeta(); return [m.spirit.eggs, Object.keys(m.spirit.own)] }"))
    pg.click('.eggres [data-act=eggok]'); time.sleep(.3)
    pg.click('[data-act=bagitem][data-k=egg2]'); time.sleep(.3); pg.click('[data-act=eggopen]'); time.sleep(2.6); pg.screenshot(path='/tmp/egg_o4.png')
    print(errs[:3]); b.close()
