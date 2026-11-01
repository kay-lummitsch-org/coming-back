import {notifyEnquiry} from './notifications.mjs';
const reply=(body,status)=>Response.json(body,{status,headers:{'Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
export async function handleNovember(request,env,ctx,now=new Date()) {
 const url=new URL(request.url);
 if(request.method!=='POST')return reply({error:'Method not allowed'},405);
 if(now<new Date('2026-10-31T23:00:00Z')||now>=new Date('2026-11-30T23:00:00Z'))return reply({error:'Campaign closed'},410);
 if(request.headers.get('Origin')!==url.origin||request.headers.get('Sec-Fetch-Site')==='cross-site')return reply({error:'Forbidden'},403);
 if(!(request.headers.get('Content-Type')||'').startsWith('application/json'))return reply({error:'JSON required'},415);
 try {
  const reader=request.body?.getReader();if(!reader)return reply({error:'Empty request'},400);
  let size=0;const chunks=[];while(true){const {done,value}=await reader.read();if(done)break;size+=value.byteLength;if(size>10000){await reader.cancel();return reply({error:'Too large'},413);}chunks.push(value);}
  const bytes=new Uint8Array(size);let off=0;for(const c of chunks){bytes.set(c,off);off+=c.length;}
  let data;try{data=JSON.parse(new TextDecoder().decode(bytes));}catch{return reply({error:'Invalid JSON'},400);}
  if(!data||typeof data!=='object'||Array.isArray(data)||data.company||data.consent!==true)return reply({error:'Invalid form'},400);
  const clean={};for(const [key,max] of Object.entries({name:100,email:254,topic:1000,preferredDate:10,slot:20,platform:20,note:500,language:2})){
   if(typeof data[key]!=='string'||data[key].length>max||(key!=='note'&&!data[key].trim()))return reply({error:'Invalid field'},400);clean[key]=data[key].trim();
  }
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(clean.email)||!['de','en'].includes(clean.language)||!['meet','phone','other'].includes(clean.platform)||!/^2026-11-\d{2}$/.test(clean.preferredDate))return reply({error:'Invalid selection'},400);
  const date=new Date(clean.preferredDate+'T12:00:00Z');if(Number.isNaN(date.getTime())||date.toISOString().slice(0,10)!==clean.preferredDate)return reply({error:'Invalid date'},400);
  const weekend=[0,6].includes(date.getUTCDay());if(weekend?clean.slot!=='arrange':!['18:00','18:30','19:00'].includes(clean.slot))return reply({error:'Invalid time'},400);
  const earliest=weekend?new Date(clean.preferredDate+'T23:59:59+01:00'):new Date(clean.preferredDate+'T'+clean.slot+':00+01:00');if(earliest<=now)return reply({error:'Time has passed'},400);
  const mode='november-'+clean.platform;
  const region=JSON.stringify({date:clean.preferredDate,slot:clean.slot,timezone:'Europe/Zurich',note:clean.note});
  const id=crypto.randomUUID(),created=now.toISOString();
  const result=await env.RIDES_DB.batch([env.RIDES_DB.prepare('INSERT INTO enquiries (id, created, name, email, mode, topic, region, language, consent_version) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)').bind(id,created,clean.name,clean.email,mode,clean.topic,region,clean.language,'november-2026-11-01'),env.RIDES_DB.prepare('INSERT INTO notifications (enquiry_id) VALUES (?)').bind(id)]);
  if(result.some(r=>!r.success))return reply({error:'Storage unavailable'},503);
  ctx.waitUntil(notifyEnquiry(env,{id,created,...clean,mode,region}));return reply({saved:true,id},201);
 }catch{return reply({error:'Storage unavailable'},503);}
}
