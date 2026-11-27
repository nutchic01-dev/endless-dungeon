from playwright.sync_api import sync_playwright
import time, re, sys
exec(open('modes.py').read().split("with sync_playwright()")[0].replace("PRS=sys.argv[1].split(',')","PRS=['f300']"))
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    for pr in ['f300','f400']:
      for rel in [0,1]:
        for team in (['leo','lumina','ignis'],['ignis','mira','raiden']):
          pg=b.new_page(viewport={'width':390,'height':844}); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT)
          pg.goto('file:///home/claude/game/index.html'); time.sleep(1.2); pg.evaluate("()=>{ SND.set.voice=0; SND.set.mus=0; SND.set.sfx=0; }")
          pg.evaluate(SETUP,[PROF[pr],rel,TEAM]); time.sleep(2.5); pg.goto('file:///home/claude/game/index.html?a'); time.sleep(2)
          pg.evaluate("()=>{ document.querySelector('[data-act=hub][data-k=adv]').click(); document.querySelector('[data-act=dhopen]').click(); }"); time.sleep(.5)
          for hid in team:
            pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhpick]'); b&&b.click(); }"); time.sleep(.25)
            pg.evaluate("(k)=>{ const b=document.querySelector('[data-act=hvsel][data-k='+k+']'); b&&b.click(); }", hid); time.sleep(.25)
            pg.evaluate("()=>{ const b=document.querySelector('.pop [data-act=dhtog]'); b&&b.click(); }"); time.sleep(.25)
          pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhpickc]'); b&&b.click(); }"); time.sleep(.3)
          res=[]
          for k in range(6):
            pg.evaluate("()=>{ const m=loadMeta(); if (m.dh&&m.dh.tries) { m.dh.tries.n=0; storeMeta(m); } }"); time.sleep(.2)
            pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhstart]'); b&&b.click(); }"); time.sleep(.5)
            pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhskip]'); b&&b.click(); }"); time.sleep(.8)
            res.append(pg.evaluate("()=>{ const t=document.querySelector('.dhlv'), r=document.querySelector('.dhrt'), d=document.querySelector('.dhres'); return (t?t.textContent:'')+':'+(r?r.textContent.slice(0,6):'?')+':'+(d&&d.innerText.match(/ดาเมจรอบนี้ ([\\d,]+)/)||['',''])[1]; }"))
            pg.evaluate("()=>{ const b=document.querySelector('[data-act=dhclose]'); b&&b.click(); }"); time.sleep(.4)
          r=' '.join(res)
          print(pr,'relic' if rel else 'norelic',team,'|',r,errs[:1],flush=True); pg.close()
    b.close()
