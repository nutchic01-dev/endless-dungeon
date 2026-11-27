from playwright.sync_api import sync_playwright
import time, re, sys
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
JS=r"""(ms)=>{ let fights=0, ults=0, longF=0, longU=0; UI.playBattle=(res,mons,finish)=>{ fights++; const u=res.frames.filter(f=>f.type==='ult'&&f.from!=null).length; ults+=u; if (res.frames.length>25){ longF++; longU+=u>0?1:0; } finish(); };
  const t0=Date.now(); while(Date.now()-t0<ms){ newRun(true); S.phase='walk'; let g=0; while(!S.over&&g++<3000){ try{
    if (S.pendingClass){ pickClass(['tank','support'][Math.random()*2|0]); continue; } if (S.pendingParty){ pickParty(['support','support']); continue; }
    if (S.pendingAwaken){ const c=awakenCandidates(); if (c.length) awaken(c[0]); else S.pendingAwaken=false; continue; } if (S.pendingChar){ rollChars(); continue; } if (S.reveal){ S.reveal=null; continue; }
    if (S.phase==='walk') step(); else if (S.phase==='event'){ const cs=S.ev.choices.filter(c=>!c.disabled); if(!cs.length){S.phase='walk';S.ev=null;continue;} cs[Math.random()*cs.length|0].fn(); } else S.phase='walk';
    if(!S.over) S.hp=Math.max(S.hp,stats().maxhp*0.6); if (S.floor>300) endRun(false,'x'); }catch(e){ S.phase='walk'; S.ev=null; } } }
  return {fights, ultPerFight:+(ults/fights).toFixed(2), longFightsWithUlt:+(longU/Math.max(1,longF)).toFixed(2), longF}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(); pg.add_init_script(INIT); pg.goto(sys.argv[1]); time.sleep(1.5)
    pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
    print(pg.evaluate(JS,20000)); b.close()
