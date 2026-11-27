from playwright.sync_api import sync_playwright
import time, json
INIT="localStorage.setItem('dq_guest','1');document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#dqload{display:none!important}#tut{display:none!important}';document.head.appendChild(s)});"
rows=[{"user_id":"a","score":259096,"name":"ReDDeVilS","hero":None,"detail":{"floor":352,"lv":80,"win":True,"pf":{"av":"leo","fr":"dragonk","nf":"srisakdi","nc":"rainbow","bg":"royal"}}},
      {"user_id":"b","score":217032,"name":"ไปเรือย","hero":"nameless","detail":{"floor":253,"lv":80,"win":True,"pf":{"av":"cls:mage","fr":"demon","nf":"chakra","nc":"ice","bg":"galaxy"}}},
      {"user_id":"c","score":187744,"name":"มารสวรรค์","hero":"luna","detail":{"floor":237,"lv":80,"win":True,"pf":{"av":"luna","fr":"angel","nf":"chonburi","nc":"moonriver","bg":"loykrathong"}}},
      {"user_id":"d","score":149412,"name":"ผู้กล้าตุ๋ยดุ๋ย","hero":"celeste","detail":{"floor":357,"lv":80,"win":True,"pf":{"av":"celeste","fr":"kranok","nf":"pattaya","nc":"champday","bg":"night"}}},
      {"user_id":"e","score":64564,"name":"ผู้กล้า","hero":"mira","detail":{"floor":140,"lv":69,"win":True,"pf":{"av":"mira","fr":"thunder","nf":"mitr","nc":"sky","bg":"sakura"}}},
      {"user_id":"f","score":62574,"name":"ผู้กล้า","hero":"finn","detail":{"floor":133,"lv":64,"win":True}}]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    ctx=b.new_context(viewport={'width':390,'height':844},device_scale_factor=2); pg=ctx.new_page(); pg.add_init_script(INIT); errs=[]
    pg.on('pageerror',lambda e: errs.append(str(e)[:300]))
    pg.route("**/rest/v1/leaderboard*", lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps(rows)))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{const m=loadMeta(); m.name='ผู้กล้าตุ๋ยดุ๋ย'; m.medals=50000; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611']}; m.ach={rkBest:1, rq:{frost:1}, dRank:{day:dayKey(),rank:1}}; storeMeta(m);}"); time.sleep(3)
    pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
    pg.evaluate("()=>document.querySelector('[data-act=avpick]').click()"); time.sleep(0.4)
    pg.evaluate("()=>document.querySelector('[data-act=cosopen]').click()"); time.sleep(0.4)
    pg.evaluate("()=>document.querySelector('[data-act=cosuse][data-k=dragonk]').click()"); time.sleep(0.5)
    pg.screenshot(path='/tmp/f6a.png')
    pg.evaluate("()=>{const g=document.querySelector('.cosgrid'); g.scrollTop=900;}"); time.sleep(0.3); pg.screenshot(path='/tmp/f6b.png')
    pg.evaluate("()=>document.querySelector('.cospop [data-act=coscl].choice').click()"); time.sleep(0.4)
    pg.evaluate("()=>{ const e=document.querySelector('[data-act=hub][data-k=rank]'); e&&e.click(); }"); time.sleep(2.5)
    pg.evaluate("()=>{const e=document.querySelector('.rkl'); e&&e.scrollIntoView({block:'center'})}"); time.sleep(0.6)
    pg.screenshot(path='/tmp/f6c.png')
    print(errs); b.close()
