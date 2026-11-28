from playwright.sync_api import sync_playwright
import time,re,sys
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
night=sys.argv[1]=='n'; sub=int(sys.argv[2]); st=int(sys.argv[3]); tag=sys.argv[4]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':760},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    if night: pg.add_init_script("Date.prototype.getHours=function(){return 21;}")
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate(f"()=>{{ const m=loadMeta(); m.name='ทดสอบ'; m.tut={{home:1}}; m.login={{last:dayKey(),streak:1}}; m.mail={{got:['gift_bug_2611','gift_leo_2611','gift_d3_2811'],dyn:[]}}; m.idle.st={st}; m.idle.sub={sub}; storeMeta(m); }}"); time.sleep(.8)
        pg.goto(f'file:///home/claude/game/index.html?w{i}'); time.sleep(3)
        if pg.evaluate("()=>loadMeta().idle.sub")==sub: break
    time.sleep(6); pg.screenshot(path=f'/tmp/{tag}.png')
    fr=[]
    for f in range(20): pg.screenshot(path=f'/tmp/{tag}_{f}.png', clip={'x':0,'y':380,'width':390,'height':170}); time.sleep(0.08)
    print(errs[:3]); b.close()
