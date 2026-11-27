from playwright.sync_api import sync_playwright
import time, re, base64, struct, numpy as np, sys
src=open('lf.py').read(); INIT=re.search(r'INIT="(.*?)"\n',src).group(1)
JOBS=[('town','town',20),('adv:forest','adv_forest',20),('adv:desert','adv_desert',20),('adv:lava','adv_lava',20),('adv:ice','adv_ice',20),('battle:forest','battle_forest',20),('battle:lava','battle_lava',20),('boss:castle','boss_castle',22),('arena','arena',20),('dragon','dragon',20)]
FX=[['hit',0.2],['slash',0.9],['crit',1.7],['fire',3.0],['ice',4.0],['thunder',5.0],['dark',6.2],['charge',7.4],['ulthit',8.15],['combo',10],['dodge',11],['revive',12],['kill',14],['legend',15],['win',17.5]]
JS="""async ([k,sec,fx])=>{ const b=await SND._render(k,sec,fx); const L=b.getChannelData(0), R=b.getChannelData(1), n=L.length; const out=new Int16Array(n*2); let pk=0, ss=0;
 for (let i=0;i<n;i++){ const l=L[i], r=R[i]; pk=Math.max(pk,Math.abs(l),Math.abs(r)); ss+=l*l; out[2*i]=Math.max(-1,Math.min(1,l))*32767; out[2*i+1]=Math.max(-1,Math.min(1,r))*32767; }
 let s=''; const u=new Uint8Array(out.buffer); for (let i=0;i<u.length;i+=32768) s+=String.fromCharCode.apply(null,u.subarray(i,i+32768)); return [btoa(s), pk, Math.sqrt(ss/n)]; }"""
def wav(path,data):
    with open(path,'wb') as f:
        f.write(b'RIFF'+struct.pack('<I',36+len(data))+b'WAVEfmt '+struct.pack('<IHHIIHH',16,1,2,44100,44100*4,4,16)+b'data'+struct.pack('<I',len(data))+data)
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome', args=['--no-sandbox','--mute-audio'])
    pg=b.new_page(); errs=[]; pg.on('pageerror',lambda e: errs.append(str(e))); pg.add_init_script(INIT); pg.goto('file:///home/claude/game/index.html'); time.sleep(1.5)
    for key,name,sec in JOBS+[(None,'sfx_demo',19)]:
        t0=time.time(); d,pk,rms=pg.evaluate(JS,[key,sec,FX if key is None else []])
        wav(f'/home/claude/dl/snd/{name}.wav',base64.b64decode(d)); print(f'{name:14s} peak {pk:.2f} rms {rms:.3f} render {time.time()-t0:.1f}s',flush=True)
    print(errs[:3]); b.close()
