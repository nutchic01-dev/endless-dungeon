from playwright.sync_api import sync_playwright
import time, json, re
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
JS=r"""(ms)=>{ const out={}; UI.playBattle=(res,mons,finish)=>{ finish(); }; const t0=Date.now(); const marks=[60,100,150,200,250,300,350,400];
  while (Date.now()-t0<ms){ newRun(true); S.phase='walk'; let g=0;
    while(!S.over && g++<5000){ try{
      if (S.pendingClass){ const ks=Object.keys(CHARS); pickClass(ks[Math.floor(Math.random()*ks.length)]); continue; }
      if (S.pendingParty){ const ks=Object.keys(CHARS); pickParty([ks[0],ks[1]]); continue; }
      if (S.pendingAwaken){ const c=awakenCandidates(); if (c.length) awaken(c[0]); else S.pendingAwaken=false; continue; }
      if (S.pendingChar){ rollChars(); continue; } if (S.reveal){ S.reveal=null; continue; }
      if (S.phase==='walk'){ step(); if (S.char && marks.includes(S.floor)){ const s=snapshot(); (out[S.floor]=out[S.floor]||[]).push([s.power,s.lv,s.st.maxhp,Math.max(s.st.atk,s.st.matk),s.st.def+s.st.mdef,s.st.cri,s.st.cridmg,s.st.pen,s.passives.length,Object.keys(s.gear).length]); } }
      else if (S.phase==='event'){ const cs=S.ev.choices.filter(c=>!c.disabled); if(!cs.length){S.phase='walk';S.ev=null;continue;} cs[Math.floor(Math.random()*cs.length)].fn(); }
      else S.phase='walk';
      if (!S.over) S.hp=Math.max(S.hp, stats().maxhp*0.6); if (S.floor>410) endRun(false,'cap');
    }catch(e){ S.phase='walk'; S.ev=null; } } }
  return out; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(); pg.add_init_script(INIT); pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
    r={}
    for i in range(5):
        o=pg.evaluate(JS,10000)
        for k,v in o.items(): r.setdefault(k,[]).extend(v)
    import statistics as stt
    print('f: n power lv hp atk def2 cri cridmg pen passives gear')
    for f in sorted(r,key=int):
        a=r[f]; print(f,len(a),[round(stt.median([x[j] for x in a]),1) for j in range(len(a[0]))])
    b.close()
