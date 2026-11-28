from playwright.sync_api import sync_playwright
import time,re,sys
INIT=re.search(r'INIT="(.*?)"\n',open('lf.py').read()).group(1)
st=int(sys.argv[1]) if len(sys.argv)>1 else 4
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio']); pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for k in sys.argv[2:] or ['a','b','c']:
        for i in range(3):
            pg.evaluate(f"()=>{{ localStorage.setItem('dq_plaza','{k}'); const m=loadMeta(); m.name='ผู้กล้านอนน้อย'; m.tut={{home:1}}; m.login={{last:dayKey(),streak:1}}; m.idle.st={st}; m.idle.sub=4; m.idle.best=90; ['leo','lumina','nyx','titan','raven','mira'].forEach(id=>{{ if(ALLCHARS[id]) m.chars[id]={{star:3,form:false,recs:[],main:0}}; }}); m.spirit={{own:{{daopui:{{lv:5,st:2,cp:0}},kitsune:{{lv:3,st:1,cp:0}}}},eq:{{ht:'daopui',dh:null,city:'kitsune'}},ess:20,nest:{{day:'',left:3,best:0}}}}; m.idle.hero=Object.assign(m.idle.hero||{{}},{{tank:'leo',support:'lumina',mage:'nyx',warrior:'titan',archer:'raven',assassin:'mira'}}); storeMeta(m); }}"); time.sleep(.8)
            pg.goto(f'file:///home/claude/game/index.html?{k}{i}'); time.sleep(2.5)
            if pg.evaluate("()=>loadMeta().idle.st")==st: break
        time.sleep(7); pg.screenshot(path=f'/tmp/pz_{k}.png')
    print(errs[:3]); b.close()
