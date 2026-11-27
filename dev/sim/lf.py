from playwright.sync_api import sync_playwright
import time, json
INIT="localStorage.setItem('dq_guest','1');document.addEventListener('DOMContentLoaded',()=>{const s=document.createElement('style');s.textContent='#dqload{display:none!important}#tut{display:none!important}';document.head.appendChild(s)});"
JS=r"""(ms)=>{ const R={}; const rep=(k,d)=>{ if(!R[k]) R[k]={n:0,d}; R[k].n++; };
  const saveUI=UI.playBattle; UI.playBattle=(res,mons,finish)=>{ finish(); };
  const t0=Date.now(); let runs=0, floors=0, wins=0, maxF=0; const A=Object.keys(ALLCHARS);
  while (Date.now()-t0<ms){
    runs++; newRun(true); if (Math.random()<0.15) { try{ startDaily(); }catch(e){} } S.phase='walk';
    let guard=0;
    while (!S.over && guard++<4000){
      try{
        // pending choices (class/party/char/awaken)
        if (S.pendingClass){ const ks=Object.keys(CHARS).concat(['villager']); pickClass(ks[Math.floor(Math.random()*ks.length)]); continue; }
        if (S.pendingParty){ const ks=Object.keys(CHARS); const pl=[]; while(pl.length<2){ const k=ks[Math.floor(Math.random()*ks.length)]; pl.push(k);} pickParty(pl); continue; }
        if (S.pendingAwaken){ const c=awakenCandidates(); if (c.length) awaken(c[Math.floor(Math.random()*c.length)]); else { S.pendingAwaken=false; rep('awaken no candidates',''); } continue; }
        if (S.pendingChar){ rollChars(); continue; }
        if (S.reveal){ S.reveal=null; continue; }
        if (S.phase==='walk'){ const f=S.floor; step(); floors++; if (S.floor!==f+1 && !S.over) rep('floor jump',f+'->'+S.floor); }
        else if (S.phase==='event'){ const ev=S.ev; if (!ev){ rep('event w/o ev',''); S.phase='walk'; continue; }
          const cs=ev.choices.filter(c=>!c.disabled); if (!cs.length){ rep('no choice: '+(ev.type||'')+' '+ev.title, ev.choices.map(c=>c.label).join('/')); S.phase='walk'; S.ev=null; continue; }
          const c=cs[Math.floor(Math.random()*cs.length)]; c.fn();
          if (S.ev===ev && S.phase==='event') rep('same event: '+(ev.type||'')+' / '+ev.title+' / '+c.label,'f'+S.floor);
        }
        else if (S.phase==='battle'){ rep('stuck battle phase',''); S.phase='walk'; }
        else { rep('phase '+S.phase,''); S.phase='walk'; }
        const st=stats(); for (const k of ['maxhp','atk','matk','def','mdef','cri','cridmg','pen','spd']) if (!isFinite(st[k])) rep('stat NaN '+k, S.cls+' f'+S.floor);
        if (!isFinite(S.gold)||S.gold<0) rep('gold bad', S.gold); if (!isFinite(S.hp)) rep('hp NaN', S.cls);
        if (S.q && S.q.id!=='destiny' && QUESTS[S.q.id] && S.q.step>=QUESTS[S.q.id].steps.length) rep('quest step overflow', JSON.stringify(S.q));
        if (S.hp<=0 && !S.over) rep('hp<=0 not dead', S.phase);
        if (!S.over && Math.random()<0.6) S.hp=Math.max(S.hp, stats().maxhp*0.5);
        if (S.floor>420) endRun(false,'cap');
      }catch(e){ rep('THROW '+String(e).slice(0,140), (e.stack||'').split('\n').slice(1,4).map(x=>x.trim()).join(' < ')); try{ S.phase='walk'; S.ev=null; }catch(_){} }
    }
    maxF=Math.max(maxF,S.floor); if (S.over&&S.over.win) wins++;
  }
  UI.playBattle=saveUI; return {R,runs,floors,wins,maxF}; }"""
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(); pg.add_init_script(INIT); errs={}
    pg.on('pageerror',lambda e: errs.__setitem__(str(e)[:200], errs.get(str(e)[:200],0)+1))
    pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
    tot={}
    for r in range(4):
        res=pg.evaluate(JS,15000)
        for k,v in res['R'].items():
            if k in tot: tot[k]['n']+=v['n']
            else: tot[k]=v
        print('round',r,{k:res[k] for k in ['runs','floors','wins','maxF']},flush=True)
    print('=== ISSUES ===')
    for k,v in sorted(tot.items(),key=lambda x:-x[1]['n']): print(v['n'],'|',k,'|',str(v['d'])[:220])
    print('=== PAGE ERRORS ===')
    for k,v in errs.items(): print(v,k)
    b.close()
