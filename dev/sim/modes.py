from playwright.sync_api import sync_playwright
import time, re, json
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
PROF={'f300':dict(atk=1500,hp=9000,cri=22,cd=205,pen=10,pas=3,pl=6,gs=[['weapon','brave'],['helm','brave'],['armor','brave'],['boots','brave'],['acc','feather',2,4]]),
      'f400':dict(atk=2200,hp=12500,cri=26,cd=215,pen=13,pas=4,pl=8,gs=[['weapon','brave'],['helm','brave'],['armor','brave'],['boots','brave'],['acc','feather',2,6],['acc','luck',2,6]])}
import sys
PRS=sys.argv[1].split(',')
TEAM=['leo','lumina','ignis','mira','raiden']
SETUP="""([P,REL,TEAM])=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; m.chars={};
  const gear={}; P.gs.forEach((x,i)=>gear['g'+i]=x[0]==='acc'?{name:'a',r:x[2],plus:x[3],acc:x[1],slot:'acc'}:{name:'x',r:3,plus:P.pl,set:x[1],slot:x[0]});
  TEAM.forEach(id=>m.chars[id]={star:3,form:false,main:0,recs:[{power:1,lv:100,floor:350,boss:300,st:{maxhp:P.hp,atk:P.atk,matk:P.atk,def:P.atk*0.7,mdef:P.atk*0.6,cri:P.cri,cridmg:P.cd,pen:P.pen,spd:105,type:'phy'},gear,skills:[{name:'a',lv:4},{name:'b',lv:4}],passives:Array(P.pas).fill('vital')}]});
  m.relics=REL?TEAM.map(id=>({uid:'r'+id,id,t:2,lv:5,subs:[{k:'cri',v:4}],on:id})):[]; m.ht={best:0,team:TEAM.slice(),en:999}; storeMeta(m); }"""
HT="""()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click();
  let last=0, lose=0, f=1, stars=0, fails=[]; while (f<=100){ { const mm=loadMeta(); mm.ht.en=999; storeMeta(mm); } window.__ht.htStart(f); const F=window.__ht.F(); if (!F) { fails.push('nostart'+f); break; } clearInterval(F.iv); let n=0; while(!F.done && n<6000){ window.__ht.htTick(); n++; }
    if (F.win){ last=f; f++; lose=0; } else { lose++; fails.push(f+(F.t>=118?'t':'d')); if (lose>=3) break; } }
  return {reached:last, fails:fails.slice(-3)}; }"""
NEST="""(t)=>{ const r=[]; for (let lv=1; lv<=10; lv++){ const m=loadMeta(); const S0=m.sp||{}; window.__ht.htStart(lv*5, {t:lv, title:'nest', W:window.__ht.nestWaves(lv), time:90, end:()=>{}, kind:'boss'}); const F=window.__ht.F(); clearInterval(F.iv); let n=0; while(!F.done&&n<6000){ window.__ht.htTick(); n++; } r.push(lv+':'+(F.win?'W'+Math.round(F.t):'L'+(F.t>=88?'t':'d'))); } return r; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    for pr in PRS:
      for rel in [0,1]:
        pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
        pg.goto('file:///home/claude/game/index.html'); time.sleep(1.2); pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
        pg.evaluate(SETUP,[PROF[pr],rel,TEAM]); time.sleep(2.5); pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
        ht=pg.evaluate(HT); nest=pg.evaluate(NEST,0) if pg.evaluate("()=>!!window.__ht.nestWaves") else 'n/a'
        print(pr,'relic' if rel else 'norelic','| hundred:',ht,'| nest:',nest, errs[:2], flush=True); pg.close()
    b.close()
