from playwright.sync_api import sync_playwright
import time, re, json
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
MOCK=r"""()=>{ const U='a1b2c3d4-0000-4000-8000-1234567890ab';
 const pf=(av,fr,hof,extra)=>({av,fm:false,fr,nf:'mitr',nc:'white',bg:'none',ps:Object.assign({bf:612,bs:812345,wb:50321,wk:wkNow(),w:57,hc:23,tm:[[av,1,5],['lumina',0,3],['titan',0,4]],rk:2,hof,ar:1350,ht:87},extra||{})});
 const rows=[{user_id:U,name:'ดาบเงา',score:812345,hero:'leo',detail:{floor:612,lv:88,win:1,pf:pf('leo','hofk',1)}},
  {user_id:'ffff-2',name:'มีมี่',score:700100,hero:'lumina',detail:{floor:540,lv:80,pf:pf('lumina','hofl',2)}},
  {user_id:'ffff-3',name:'ผู้กล้า',score:600000,hero:null,detail:{floor:400,lv:70}}];
 window.__dqCloud={auth:{user:{id:U}}, lbTop:async(b,p)=>{ window.__lastTop=b+'|'+p; return rows; }, lbMine:async()=>({rank:1,total:3,score:812345}), lbUser:async()=>[rows[1]], lbSync:async()=>({}), get __x(){return 1}}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for i in range(3):
        pg.evaluate("()=>{ const m=loadMeta(); m.name='ผู้กล้า'; m.tut={home:1,adv:1,run:1}; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; storeMeta(m); }"); time.sleep(1)
        pg.goto(f'file:///home/claude/game/index.html?a{i}'); time.sleep(2)
        if pg.query_selector('#nmin'): break
    pg.evaluate(MOCK); time.sleep(.3)
    pg.screenshot(path='/tmp/pc_name.png')
    pg.fill('#nmin','ผู้กล้า'); pg.click('[data-act=nmsave]'); time.sleep(.4); print('err1', pg.inner_text('.nerr') if pg.query_selector('.nerr') else None)
    pg.fill('#nmin','อัศวินแสง'); pg.click('[data-act=nmsave]'); time.sleep(.4); print('name', pg.evaluate("()=>loadMeta().name"), 'pop', bool(pg.query_selector('#nmin')))
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=hub][data-k=rank]'); if (b) b.click(); }"); time.sleep(.6)
    if not pg.query_selector('.rkew'):
        pg.evaluate("()=>{ const s=[...document.querySelectorAll('[data-act=hub]')].map(x=>x.dataset.k); window.__ks=s; }"); print(pg.evaluate("()=>window.__ks"))
    pg.screenshot(path='/tmp/pc_rank_w.png', full_page=True); print('top', pg.evaluate("()=>window.__lastTop"))
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=rkew][data-k=a]'); b&&b.click(); }"); time.sleep(.6)
    pg.screenshot(path='/tmp/pc_rank_a.png', full_page=True); print('top', pg.evaluate("()=>window.__lastTop"))
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=rkview][data-i=\"0\"]'); b&&b.click(); }"); time.sleep(.6)
    pg.screenshot(path='/tmp/pc_card.png')
    pg.evaluate("()=>{ const b=document.querySelector('[data-act=rkviewc]'); b&&b.click(); }"); time.sleep(.3)
    pg.evaluate("()=>{ const b=document.createElement('button'); b.dataset.act='pcard'; b.dataset.u='ffff-2'; b.dataset.n='มีมี่'; document.querySelector('.overlay').appendChild(b); b.click(); }"); time.sleep(.6)
    pg.screenshot(path='/tmp/pc_card2.png')
    print(errs[:5]); b.close()
