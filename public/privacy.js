(() => {
  'use strict';
  const de = document.documentElement.lang === 'de';
  const key = 'kay-privacy-v1';
  const maxAge = 180 * 24 * 60 * 60 * 1000;
  const text = de ? {
    title:'Du entscheidest.', body:'Diese Website funktioniert auch ohne Besuchsstatistik. Wenn Du zustimmst, nutzen wir Cloudflare Web Analytics, um Seitenaufrufe, Herkunftsverweise und Ladezeiten auszuwerten – ohne Analyse-Cookies.',
    extra:'Das externe Newsletter-Formular laden wir erst, wenn Du es öffnest. Deine Auswahl kannst Du jederzeit unter „Datenschutz & Einstellungen“ ändern.',
    no:'Nur notwendige Funktionen', yes:'Statistik erlauben', more:'Mehr zum Datenschutz', settings:'Datenschutz & Einstellungen', off:'Statistik deaktivieren', close:'Schliessen', onState:'Statistik ist erlaubt.', offState:'Statistik ist deaktiviert.', revoke:'Beim Deaktivieren wird die Seite neu geladen, damit der Messcode nicht weiterläuft.'
  } : {
    title:'Your choice.', body:'This website works without visitor analytics. If you agree, we use Cloudflare Web Analytics to measure page views, referral sources and loading times – without analytics cookies.',
    extra:'We only load the external newsletter form when you choose to open it. You can change your choice at any time under “Privacy & settings”.',
    no:'Necessary functions only', yes:'Allow analytics', more:'More about privacy', settings:'Privacy & settings', off:'Disable analytics', close:'Close', onState:'Analytics is allowed.', offState:'Analytics is disabled.', revoke:'Disabling analytics reloads this page so the measurement script stops running.'
  };
  let choice = null;
  try { const saved = JSON.parse(localStorage.getItem(key)); if (saved && typeof saved.analytics === 'boolean' && Date.now() - saved.at >= 0 && Date.now() - saved.at < maxAge) choice = saved.analytics; } catch (_) {}
  let loaded = false;
  function analytics() {
    if (loaded || choice !== true) return;
    loaded = true;
    const s = document.createElement('script');
    s.type = 'module'; s.src = 'https://static.cloudflareinsights.com/beacon.min.js';
    s.dataset.cfBeacon = JSON.stringify({token:'90724fe691964751a961caa791ce1974'});
    document.head.appendChild(s);
  }
  const banner = document.createElement('section');
  banner.className = 'privacy-banner'; banner.setAttribute('role','dialog'); banner.setAttribute('aria-labelledby','privacy-title');
  banner.innerHTML = `<h2 id="privacy-title">${text.title}</h2><p>${text.body}</p><p>${text.extra}</p><div class="privacy-actions"><button type="button" data-choice="no">${text.no}</button><button type="button" data-choice="yes">${text.yes}</button><a href="${de?'/de/datenschutz/':'/privacy/'}">${text.more}</a></div>`;
  document.body.appendChild(banner); banner.hidden = choice !== null;
  const dialog = document.createElement('dialog');
  dialog.className = 'privacy-settings'; dialog.setAttribute('aria-labelledby','privacy-settings-title');
  dialog.innerHTML = `<h2 id="privacy-settings-title">${text.settings}</h2><p>${text.body}</p><p data-status></p><p>${text.revoke}</p><div class="privacy-actions"><button type="button" data-choice="no">${text.off}</button><button type="button" data-choice="yes">${text.yes}</button><button type="button" data-close>${text.close}</button></div><p><a href="${de?'/de/datenschutz/':'/privacy/'}">${text.more}</a></p>`;
  document.body.appendChild(dialog);
  function setChoice(value) {
    const wasLoaded = loaded;
    choice = value;
    try { localStorage.setItem(key, JSON.stringify({analytics:value,at:Date.now()})); } catch (_) {}
    banner.hidden = true; dialog.close();
    if (value) analytics();
    else if (wasLoaded) location.reload();
  }
  for (const box of [banner,dialog]) box.addEventListener('click', e => {
    const b = e.target.closest('button[data-choice]'); if (b) setChoice(b.dataset.choice === 'yes');
  });
  dialog.querySelector('[data-close]').addEventListener('click',()=>dialog.close());
  document.querySelectorAll('[data-privacy-settings]').forEach(b=>b.addEventListener('click',()=>{
    dialog.querySelector('[data-status]').textContent = choice === true ? text.onState : text.offState;
    dialog.querySelector('[data-choice="yes"]').disabled = choice === true;
    dialog.showModal();
  }));
  document.querySelectorAll('[data-newsletter-open]').forEach(button=>button.addEventListener('click',()=>{
    const container = button.closest('.subscription-form');
    const field = document.createElement('div'); field.className='sender-form-field'; field.dataset.senderFormId='epYyZ1'; container.appendChild(field);
    button.disabled = true;
    window.Sender = 'sender';
    window.sender = window.sender || function(){(window.sender.q=window.sender.q||[]).push(arguments);};
    window.sender.l=Date.now();
    window.sender.on=function(event,callback){window.sender.listeners=window.sender.listeners||{};(window.sender.listeners[event]=window.sender.listeners[event]||[]).push(callback);};
    if (!document.querySelector('script[data-kay-sender]')) {
      const script=document.createElement('script'); script.async=true; script.src='https://cdn.sender.net/accounts_resources/universal.js'; script.dataset.kaySender='true'; document.head.appendChild(script);
      window.sender('17c1f235ed7798');
    }
  }));
  window.addEventListener('storage', event => {
    if (event.key !== key && event.key !== null) return;
    // Another tab changed or cleared consent: reload to apply the same choice.
    location.reload();
  });
  analytics();
})();
