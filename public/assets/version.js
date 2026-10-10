(()=>{'use strict';
/* v0.4.8: version label is driven by /version.json. The label is created if a page ever ships without it. */
const apply=v=>{
  let el=document.querySelector('.app-version');
  if(!el){
    const nav=document.querySelector('.bottom-nav');
    if(!nav)return;
    el=document.createElement('span');
    el.className='app-version';
    nav.append(el);
  }
  el.textContent='v'+v;
  el.setAttribute('aria-label','Application version '+v);
};
fetch('/version.json',{cache:'no-cache'})
  .then(r=>r.ok?r.json():Promise.reject(new Error('version unavailable')))
  .then(d=>{if(d&&d.version)apply(String(d.version))})
  .catch(()=>{/* keep the static label already in the page */});
})();
