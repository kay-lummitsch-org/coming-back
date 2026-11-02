(() => {
 'use strict';
 const active=()=>Date.now()>=Date.parse('2026-10-31T23:00:00Z')&&Date.now()<Date.parse('2026-11-30T23:00:00Z');
 const de=document.documentElement.lang==='de',route=de?'/de/november/':'/november/';
 const copy=de?{chip:'30 Minuten. Eine gute Frage. ↗'}:{chip:'30 minutes. One good question. ↗'};
 document.addEventListener('DOMContentLoaded',()=>{
  if(!active()){const f=document.getElementById('november-form');if(f){f.hidden=true;document.querySelector('.november-closed').hidden=false;}return;}
  const chip=document.createElement('a');chip.className='november-chip';chip.href=route;chip.textContent=copy.chip;document.body.appendChild(chip);
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
