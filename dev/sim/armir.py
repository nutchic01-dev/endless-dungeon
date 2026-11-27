from playwright.sync_api import sync_playwright
import time, json, sys
INIT="localStorage.setItem('dq_guest','1');document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#dqload{display:none!important}#tut{display:none!important}';document.head.appendChild(s)});"
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':390,'height':844}); pg.add_init_script(INIT)
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.2)
    pg.evaluate("""()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; const m=loadMeta(); Object.keys(ALLCHARS).forEach((id,i)=>m.chars[id]={star:3,form:false,recs:[],main:0}); storeMeta(m); }""")
    pg.reload(); time.sleep(1.2)
    pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=arnopen]').click(); }"); time.sleep(0.5)
    comps=[['coral','gason','serena','mira','raven'],['leo','blaze','luna','ignis','toby'],['titan','marine','panpan','kira','yami'],['brenda','raiden','lumina','finn','scorp']]
    for c in comps:
        r=pg.evaluate("""(c)=>{ const {arState,arSnap,arStart,AR}=__ar; const hubMsg_dbg=()=>document.querySelector('.hubmsg')&&document.querySelector('.hubmsg').textContent; let w=0, t=0, N=24;
          for (let it=0;it<N;it++){ const m=loadMeta(), A=arState(m); A.used=0; A.atk=c.slice(); storeMeta(m); AR.opp=[{bot:true,name:'x',rating:1000,team:arSnap(m,c),user_id:'b'}]; arStart(0); const F=__ar.F(); if(!F) return ['nofight', it, hubMsg_dbg()];
            F.skip=true; const sf=SND.sfx; SND.sfx=()=>{}; let g=0; while(!F.done&&g++<40000) __ar.tick(); SND.sfx=sf; if (F.win) w++; t+=F.t; __ar.clr(); }
          return [w+'/'+N, Math.round(t/N), c]; }""", c)
        print(r)
    b.close()
