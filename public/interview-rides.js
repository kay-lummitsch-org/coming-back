'use strict';
const rideForm=document.getElementById('ride-form');
if(rideForm){
 const de=rideForm.dataset.language==='de';
 const submit=rideForm.querySelector('button[type=submit]');
 const original=submit.innerHTML;
 const error=document.getElementById('form-error');
 rideForm.addEventListener('submit',async event=>{
  event.preventDefault();
  if(!rideForm.reportValidity())return;
  const data=Object.fromEntries(new FormData(rideForm));
  data.consent=rideForm.elements.consent.checked;
  data.language=rideForm.dataset.language;
  error.hidden=true;submit.disabled=true;submit.textContent=de?'Wird gespeichert …':'Saving …';
  try{
   const response=await fetch('/api/interview-rides',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
   if(!response.ok)throw Error('Not saved');
   const result=await response.json();
   if(result.saved!==true)throw Error('Unexpected response');
   rideForm.hidden=true;document.getElementById('ride-success').hidden=false;document.getElementById('ride-success').focus();
  }catch(_){error.hidden=false;error.focus();}
  finally{submit.disabled=false;submit.innerHTML=original;}
 });
 document.getElementById('form-again').addEventListener('click',()=>{document.getElementById('ride-success').hidden=true;rideForm.hidden=false;rideForm.reset();rideForm.elements.name.focus();});
}
