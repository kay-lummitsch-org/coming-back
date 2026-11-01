(() => {
 'use strict';
 const active=()=>Date.now()>=Date.parse('2026-10-31T23:00:00Z')&&Date.now()<Date.parse('2026-11-30T23:00:00Z');
 const de=document.documentElement.lang==='de',route=de?'/de/november/':'/november/';
 const copy=de?{eyebrow:'NOVEMBER · ZEIT FÜR EIN GESPRÄCH',title:'Was steht Deinen<br>Leuten im Weg?',intro:'Im November nehme ich mir Zeit<br>für ein Gespräch mit Dir.',body:'<strong>30 Minuten.</strong> Du bringst eine konkrete Situation mit. Ich bringe Neugier mit.',terms:'Kostenlos. Unverbindlich. Vertraulich.',punch:'Und im schlimmsten Fall –<br>wird es besser:)',cta:'Lass uns reden',later:'Lieber erst mal umsehen',close:'Einladung schliessen',caption:'Fiktives KI-Cover · auf Grundlage eines Fotos von Sven Loof.',chip:'30 Minuten. Eine gute Frage. ↗'}:{eyebrow:'NOVEMBER · TIME FOR A CONVERSATION',title:'What is getting in<br>your people’s way?',intro:'This November, I’m making time<br>for a conversation with you.',body:'<strong>30 minutes.</strong> You bring a real situation. I bring curiosity.',terms:'Free. No obligation. Confidential.',punch:'And in the worst case –<br>things get better:)',cta:'Let’s talk',later:'I’ll have a look around first',close:'Close invitation',caption:'Fictional AI cover · based on a photograph by Sven Loof.',chip:'30 minutes. One good question. ↗'};
 document.addEventListener('DOMContentLoaded',()=>{
  if(!active()){const f=document.getElementById('november-form');if(f){f.hidden=true;document.querySelector('.november-closed').hidden=false;}return;}
  const home=['/','/de/'].includes(location.pathname);
  const chip=document.createElement('a');chip.className='november-chip';chip.href=route;chip.textContent=copy.chip;document.body.appendChild(chip);
  if(home){
   const modal=document.createElement('dialog');modal.className='november-overlay';modal.setAttribute('aria-labelledby','november-title');
   modal.innerHTML=`<section class="november-card"><button type="button" class="november-close" aria-label="${copy.close}">×</button><figure class="november-visual" style="margin:0"><img src="/assets/turning-sixty-rd-cover.webp" alt="${de?'Fiktives Reader’s-Digest-Cover mit Kay':'Fictional Reader’s Digest cover featuring Kay'}"><figcaption>${copy.caption}</figcaption></figure><div class="november-copy"><p class="november-eyebrow">${copy.eyebrow}</p><h2 id="november-title">${copy.title}</h2><p>${copy.intro}</p><p>${copy.body}</p><p><strong>${copy.terms}</strong></p><p class="november-punchline">${copy.punch}</p><a class="november-cta" href="${route}">${copy.cta} <span aria-hidden="true">↗</span></a><button class="november-dismiss" type="button">${copy.later}</button></div></section>`;
   document.body.appendChild(modal);
   const key='kay-november-2026-dismissed';
   const dismiss=()=>{try{localStorage.setItem(key,'yes');}catch(_){}modal.close();chip.focus();};
   modal.querySelector('.november-close').addEventListener('click',dismiss);modal.querySelector('.november-dismiss').addEventListener('click',dismiss);
   modal.addEventListener('cancel',e=>{e.preventDefault();dismiss();});modal.querySelector('.november-cta').addEventListener('click',()=>{try{localStorage.setItem(key,'yes');}catch(_){}});
   const show=()=>{let seen=false;try{seen=localStorage.getItem(key)==='yes';}catch(_){}const privacy=document.querySelector('.privacy-banner');if(!seen&&privacy&&privacy.hidden&&!modal.open)modal.showModal();};
   const privacy=document.querySelector('.privacy-banner');if(privacy)new MutationObserver(show).observe(privacy,{attributes:true,attributeFilter:['hidden']});show();
  }
  const f=document.getElementById('november-form');if(!f)return;
  const date=f.elements.preferredDate,slot=f.elements.slot,submit=f.querySelector('[type=submit]'),error=document.getElementById('november-error');
  const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Zurich',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());date.min=today>'2026-11-01'?today:'2026-11-01';
  date.addEventListener('change',()=>{const day=new Date(date.value+'T12:00:00Z').getUTCDay();const weekend=[0,6].includes(day);for(const o of slot.options){if(o.value)o.disabled=weekend?o.value!=='arrange':o.value==='arrange';}slot.value=weekend?'arrange':'';});
  f.addEventListener('submit',async event=>{
   event.preventDefault();if(!f.reportValidity())return;
   const data=Object.fromEntries(new FormData(f));data.consent=f.elements.consent.checked;data.language=f.dataset.language;
   const label=submit.textContent;submit.disabled=true;submit.textContent=de?'Wird gespeichert …':'Saving …';error.hidden=true;
   try{const response=await fetch('/api/november',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});if(!response.ok)throw Error('not saved');const result=await response.json();if(result.saved!==true)throw Error('not saved');f.hidden=true;const success=document.getElementById('november-success');success.hidden=false;success.focus();}
   catch(_){error.textContent=de?'Die Anfrage konnte nicht gespeichert werden. Bitte prüfe Datum und Zeit oder schreibe an kay@kaylummitsch.com.':'Your request could not be saved. Please check the date and time or email kay@kaylummitsch.com.';error.hidden=false;error.focus();}
   finally{submit.disabled=false;submit.textContent=label;}
  });
 });
})();
