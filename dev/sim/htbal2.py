from playwright.sync_api import sync_playwright
import time, sys
PROF={'none':None,
 'f100':dict(atk=600,hp=3500,cri=12,cd=170,pen=3,pas=2,g=3,pl=3,gs=[['weapon','brave'],['armor','brave'],['acc','luck',1,2]]),
 'f300':dict(atk=1500,hp=9000,cri=22,cd=205,pen=10,pas=3,g=5,pl=6,gs=[['weapon','brave'],['helm','brave'],['armor','brave'],['boots','brave'],['acc','feather',2,4]]),
 'f450':dict(atk=2800,hp=15000,cri=30,cd=230,pen=15,pas=4,g=6,pl=9,gs=[['weapon','pierce'],['helm','pierce'],['armor','pierce'],['boots','pierce'],['acc','feather',3,9],['acc','hammer',3,9]])}
import sys
REL=1; G=None
CASES=[(5,True,'none'),(5,True,'f100'),(5,True,'f300'),(5,True,'f450')]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(viewport={'width':375,'height':740}); pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
    for st,form,pr in CASES:
        r=pg.evaluate("""([st,form,P,REL,G])=>{ const m=loadMeta(); m.chars={}; const ids=Object.keys(ALLCHARS);
          const mk=id=>{ if(!P) return []; const gear={}; (P.gs||[]).forEach((x,i)=>gear['g'+i]=x[0]==='acc'?{name:'a',r:x[2],plus:x[3],acc:x[1],slot:'acc'}:{name:'x',r:3,plus:P.pl,set:x[1],slot:x[0]});
            return [{power:1,lv:100,floor:1,boss:1,st:{maxhp:P.hp,atk:P.atk,matk:P.atk,def:P.atk*0.7,mdef:P.atk*0.6,cri:P.cri,cridmg:P.cd,pen:P.pen,spd:100,type:'phy'},gear,skills:[{name:'a',lv:4},{name:'b',lv:4}],passives:Array(P.pas).fill('vital')}]; };
          ids.forEach(id=>m.chars[id]={star:st,form,recs:mk(id),main:0}); m.ht={best:0,team:[]}; m.relics=REL?ids.map(id=>({uid:'r'+id,id,t:4,lv:10,subs:[{k:'cri',v:6},{k:'spd',v:4}],on:id})):[]; if(G) {window.__htg[0]=G[0];window.__htg[1]=G[1];} storeMeta(m);
          document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click(); document.querySelector('[data-act=htauto]').click();
          let last=0, lose=0, f=1; while (f<=100){ { const mm=loadMeta(); mm.ht.en=999; storeMeta(mm); } window.__ht.htStart(f); const F=window.__ht.F(); clearInterval(F.iv); let n=0; while(!F.done && n<6000){ window.__ht.htTick(); n++; }
            if (F.win){ last=f; f++; lose=0; } else { lose++; if (lose>=3) break; } }
          const pw=heroPw(loadMeta(),ids[0]); return [last, +pw.recP.dps.toFixed(2), +pw.recP.hp.toFixed(2)]; }""",[st,form,PROF[pr],REL,G])
        print(st,form,pr,'-> reached',r,flush=True)
    b.close()
