const fs=require('fs');
const code=fs.readFileSync(process.argv[2],'utf8').split('<script>').map(x=>x.split('</script>')[0]).find(x=>x.includes('function newRun'));
const N=+(process.argv[3]||400); const mode=process.argv[4]||'mixed'; const over=process.argv[5]||'';
const out = new Function(code+`
${over}
const CL=['tank','warrior','mage','support','archer','assassin'];
const ST={breaks:0, enh:0, maxPlus:0}; const BL=[];
function act(){
  for (let guard=0; guard<40 && S.phase==='event' && S.ev && !S.over; guard++){
    const e=S.ev, ch=e.choices.filter(c=>!c.disabled), t=e.type, hpP=S.hp/stats().maxhp; let c=ch[0];
    if(t==='boss'){ const est=+e.choices[0].sub.match(/\\d+/)[0]; BL.push([S.floor,est]); c=ch[0]; }
    else if(t==='badMon') c=ch[ch.length-1];
    else if(t==='mPotion') c = hpP<0.5 && !ch[0].label.includes('ไม่')? ch[0] : ch[ch.length-1];
    else if(t==='chest') c = hpP>0.6? (ch[1]||ch[0]) : ch[0];
    else if(t==='training') c=pick(ch);
    else if(t==='offer'){ const it=e.item; const slots=it.slot==='acc'?(S.acc2?['acc','acc2']:['acc']):[it.slot];
      let best=-1,bi=-1; slots.forEach((s,i)=>{ const d=itemScore(it)-itemScore(S.gear[s]); if(d>best){best=d;bi=i;} });
      c = best>0 ? e.choices[bi] : e.choices[e.choices.length-1]; }
    else if(t==='mEquip'){
      if (e.enhancing){ const it=S.gear[e.enhancing]; if(!it){ c=e.choices[e.choices.length-1]; } else {
          const prot = it.plus>=3; const want = it.plus < 7;
          if (want && prot && !e.choices[1].disabled && S.gold>e.cost*3+50) c=e.choices[1];
          else if (want && !prot && !e.choices[0].disabled) c=e.choices[0];
          else { S.shop=null; done('leave'); break; } } }
      else if (e.title==='ตีบวกอุปกรณ์'){ const opts=e.choices.filter(x=>x.slot); const w=opts.find(x=>x.slot==='weapon')||opts[0];
          c = w && S.gold>enhCost(S.gear[w.slot])*(S.gear[w.slot].plus>=3?3:1) ? w : e.choices[e.choices.length-1]; if(c.back){ S.shop=null; done('leave'); break; } }
      else { const buys=e.choices.filter(x=>x.item && !x.disabled && itemScore(x.item)>itemScore(S.gear[x.item.slot==='acc'?'acc':x.item.slot]));
          if (buys.length) c=buys[0]; else { const enh=e.choices.find(x=>x.enh&&!x.disabled); c = (enh && S.gold>150 && !e._tried) ? enh : e.choices.find(x=>x.leave); if(c===enh) e._tried=true; } }
    }
    const before = S.gear && e.enhancing ? S.gear[e.enhancing] : null;
    c.fn();
    if (e.enhancing && before){ ST.enh++; if(!S.gear[e.enhancing]) ST.breaks++; else ST.maxPlus=Math.max(ST.maxPlus,S.gear[e.enhancing].plus); }
  }
}
return {ST, BL, run(mode){
  newRun(); let g=0;
  while(!S.over && g++<5000){
    if(S.pendingClass) pickClass(mode==='vil'?'villager':mode.startsWith('f:')?mode.split(':')[1]:pick(CL));
    if(S.pendingParty) pickParty(shuffle(CL.filter(c=>c!==S.cls)).slice(0,2));
    if(S.pendingChar) rollChars(mode.startsWith('f:')?mode.split(':')[2]:undefined);
    if(S.pendingAwaken) awaken(pick(awakenCandidates()));
    S.reveal=null; step(); act();
  }
  return {ch:S.char?S.char.id:'-', books:S.st.books||0, sl:S.skillLv.join(''), combos:S.st.combos||0, floor:S.floor, lv:S.lv, win:!!(S.over&&S.over.win), cls:S.cls, gs:gearScore(), gold:S.gold, cause:S.over&&S.over.cause};
}};`)();
const res=[];for(let i=0;i<N;i++)res.push(out.run(mode));
const q=(a,p)=>{a=a.slice().sort((x,y)=>x-y);return a[Math.floor(p*(a.length-1))];};

const fought=res.filter(r=>r.win||/บอส|ราชา|ราชินี|มังกร|เทวทูต|ราชันย์/.test(r.cause||''));
console.log('N',N,'win',res.filter(r=>r.win).length,'bossLoss',fought.length-res.filter(r=>r.win).length,'diedBefore',N-fought.length);
const bins={};fought.forEach(r=>{const b=Math.floor(r.floor/25)*25;(bins[b]=bins[b]||[0,0]);bins[b][0]++;if(r.win)bins[b][1]++;});
console.log(Object.entries(bins).map(([k,v])=>k+'-'+(+k+24)+': '+v[1]+'/'+v[0]+' ('+(v[1]/v[0]*100).toFixed(0)+'%)').join('  '));
const cc={};res.filter(r=>!r.win).forEach(r=>cc[r.cause]=(cc[r.cause]||0)+1);console.log(Object.entries(cc).sort((a,b)=>b[1]-a[1]).slice(0,12));
const B=out.BL, bb={}; B.forEach(([f,e])=>{const k=Math.floor(f/50)*50;(bb[k]=bb[k]||[]).push(e);});
console.log('est by floor:',Object.entries(bb).map(([k,v])=>k+': n'+v.length+' avg'+(v.reduce((a,b)=>a+b,0)/v.length).toFixed(0)+'%').join(' | '));
