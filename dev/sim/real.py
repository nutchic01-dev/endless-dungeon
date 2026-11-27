from playwright.sync_api import sync_playwright
import time, re, sys, json
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
def g(slot,r,plus,set=None,acc=None): return dict(slot=slot,r=r,plus=plus,set=set,acc=acc,name='x')
R1=dict(lv=98,floor=354,st=dict(maxhp=12961,atk=2898,matk=300,def_=1697,mdef=685,cri=39.6,cridmg=256,pen=8.2,type='phy'),gear=[g('weapon',3,7,'blood'),g('helm',1,0,'blood'),g('armor',2,5,'blood'),g('boots',2,7,'blood'),g('acc',3,5,acc='ring')],sk=[5,5,5],pas=1)
R2=dict(lv=98,floor=441,st=dict(maxhp=23154,atk=4226,matk=300,def_=1398,mdef=1545,cri=26,cridmg=274,pen=21,type='phy'),gear=[g('acc',3,7,acc='compass'),g('acc2',1,0,acc='cloak'),g('helm',3,6,'eternal'),g('armor',3,0,'pierce'),g('boots',1,0,'hunter'),g('weapon',2,7,'phoenix')],sk=[1,1,1],pas=1)
R3=dict(lv=100,floor=389,st=dict(maxhp=9864,atk=300,matk=3814,def_=952,mdef=718,cri=45,cridmg=223,pen=17,type='mag'),gear=[g('acc',3,4,acc='luck'),g('helm',2,5,'sage'),g('armor',1,3,'sage'),g('boots',2,5,'sage'),g('weapon',2,0,'healer')],sk=[5,5,5],pas=1)
R4=dict(lv=100,floor=334,st=dict(maxhp=10172,atk=2555,matk=300,def_=1544,mdef=1190,cri=5,cridmg=198,pen=2,type='phy'),gear=[g('acc',3,1,acc='feather'),g('helm',2,0,'brave'),g('armor',3,1,'brave'),g('boots',2,3,'brave'),g('weapon',2,4,'brave')],sk=[5,5,5],pas=1)
TEAM={'leo':R4,'lumina':R3,'nameless':R2,'sage':R3,'kira':R1}
SETUP="""([T,STAR,REL])=>{ const m=loadMeta(); m.name='x'; m.login={last:dayKey(),streak:1}; m.mail={got:['gift_bug_2611','gift_leo_2611'],dyn:[]}; m.chars={};
  Object.entries(T).forEach(([id,R])=>{ const gear={}; R.gear.forEach((x,i)=>gear['g'+i]=x); const st=Object.assign({},R.st,{def:R.st.def_}); delete st.def_;
    m.chars[id]={star:STAR,form:false,main:0,recs:[{power:1,lv:R.lv,floor:R.floor,boss:20,st,gear,skills:R.sk.map(l=>({name:'s',lv:l})),passives:Array(R.pas).fill('vital')}]}; });
  const ids=Object.keys(T); m.relics=REL?ids.map(id=>({uid:'r'+id,id,t:2,lv:5,subs:[{k:'cri',v:4}],on:id})):[]; m.ht={best:0,team:ids,en:999}; storeMeta(m); }"""
HT="""()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=htopen]').click();
  let last=0, lose=0, f=1, fails=[]; while (f<=100){ { const mm=loadMeta(); if (mm.ht) { mm.ht.en=999; storeMeta(mm); } } window.__ht.htStart(f); const F=window.__ht.F(); if (!F){ fails.push('ns'+f); break; } clearInterval(F.iv); let n=0; while(!F.done && n<6000){ window.__ht.htTick(); n++; }
    if (F.win){ last=f; f++; lose=0; } else { lose++; fails.push(f+(F.t>=118?'t':'d')); if (lose>=3) break; } }
  return {reached:last, fails:fails.slice(-3)}; }"""
NEST="""()=>{ const r=[]; for (let lv=1; lv<=10; lv++){ window.__ht.htStart(lv*5, {t:lv, title:'nest', W:window.__ht.nestWaves(lv), time:90, end:()=>{}, kind:'boss'}); const F=window.__ht.F(); if (!F){ r.push(lv+'ns'); continue; } clearInterval(F.iv); let n=0; while(!F.done&&n<6000){ window.__ht.htTick(); n++; } r.push(lv+(F.win?'W'+Math.round(F.t):'L')); } return r.join(' '); }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    for star,rel in [(3,0),(3,1)]:
        pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
        pg.goto('file:///home/claude/game/index.html'); time.sleep(1.2); pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
        for tr in range(4):
            pg.evaluate(SETUP,[TEAM,star,rel]); time.sleep(2.5); pg.goto('file:///home/claude/game/index.html?a'+str(tr)); time.sleep(2)
            ok=pg.evaluate("(st)=>{ const m=loadMeta(); return !!(m.ht&&m.ht.team&&m.ht.team.length===5&&m.chars.leo&&m.chars.leo.star===st); }",star)
            if ok: break
        ht=pg.evaluate(HT); nest=pg.evaluate(NEST)
        print(f'{star}star relic{rel} | hundred {ht} | nest {nest}', errs[:1], flush=True); pg.close()
    b.close()
