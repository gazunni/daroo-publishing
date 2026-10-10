(()=>{'use strict';
const $=id=>document.getElementById(id),stage=$('stage'),seek=$('seek'),counter=$('counter');
const params=new URLSearchParams(location.search),id=params.get('book')||'gabe-and-jinx-01';
const catalog={'gabe-and-jinx-01':'/books/gabe-and-jinx/book-01/manifest.json'};
let book,index=0,spread=false,scale=1,panX=0,panY=0,gesture=null;
const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
const spreadCount=()=>spread&&window.innerWidth>=900?2:1;
const zoomed=()=>scale>1.015;
function clampPan(){const frame=stage.getBoundingClientRect();panX=clamp(panX,-frame.width*(scale-1)/2,frame.width*(scale-1)/2);panY=clamp(panY,-frame.height*(scale-1)/2,frame.height*(scale-1)/2)}
function applyZoom(){clampPan();const sheet=$('page-sheet');if(sheet)sheet.style.transform=`translate(${panX}px,${panY}px) scale(${scale})`;stage.classList.toggle('is-zoomed',zoomed());$('zoomreset').textContent=Math.round(scale*100)+'%';$('zoomout').disabled=scale<=1.001;$('zoomin').disabled=scale>=3.999}
function resetZoom(){scale=1;panX=panY=0;applyZoom()}
function setZoom(next){const was=scale;scale=clamp(next,1,4);if(scale===1){panX=panY=0}else if(was>1){panX*=scale/was;panY*=scale/was}applyZoom()}
function makePage(p){const el=document.createElement('article');el.className='reader-page';el.setAttribute('aria-label','Book page '+p.number);if(p.image){const img=document.createElement('img');img.src=p.image;img.alt=p.alt||p.title||'Development artwork';img.draggable=false;el.append(img);const folio=document.createElement('div');folio.className='reader-folio';folio.textContent='CHAPTER '+(p.chapter||1)+' · PAGE '+p.number+' OF '+book.pages.length;folio.setAttribute('aria-hidden','true');el.append(folio);if(p.caption){const cap=document.createElement('div');cap.className='page-caption';cap.textContent=p.caption;el.append(cap)}}else{el.classList.add('placeholder');const h=document.createElement('h2');h.textContent=p.title||'Preview';const d=document.createElement('p');d.textContent=p.description||'';el.append(h,d)}return el}
const imageWarmCache=new Map();
function warmAdjacentPages(){
  if(!book)return;
  const count=spreadCount();
  const candidates=[index+count,index+count+1,index-1];
  const wanted=new Set();
  for(const i of candidates){
    const src=book.pages[i]?.image;
    if(!src)continue;
    wanted.add(src);
    if(!imageWarmCache.has(src)){
      const image=document.createElement('img');
      image.decoding='async';
      image.src=src;
      imageWarmCache.set(src,image);
    }
  }
  for(const [src] of imageWarmCache){if(!wanted.has(src))imageWarmCache.delete(src)}
}
function draw(){if(!book)return;const n=spreadCount();index=clamp(index,0,Math.max(0,book.pages.length-n));stage.replaceChildren();const sheet=document.createElement('div');sheet.className='page-sheet';sheet.id='page-sheet';sheet.classList.toggle('spread',n===2);for(let i=index;i<Math.min(index+n,book.pages.length);i++)sheet.append(makePage(book.pages[i]));stage.append(sheet);counter.textContent=(index+1)+(n===2&&index+1<book.pages.length?'–'+(index+2):'')+' / '+book.pages.length;seek.value=index+1;$('prev').disabled=index===0;$('next').disabled=index+n>=book.pages.length;history.replaceState(null,'',location.pathname+'?book='+encodeURIComponent(id)+'&page='+(index+1));resetZoom();warmAdjacentPages()}
function move(delta){if(!book||zoomed())return;index=clamp(index+delta,0,Math.max(0,book.pages.length-spreadCount()));draw()}
$('prev').onclick=()=>move(-spreadCount());$('next').onclick=()=>move(spreadCount());
seek.oninput=()=>{index=Number(seek.value)-1;draw()};
$('spread').onclick=()=>{spread=!spread;$('spread').setAttribute('aria-pressed',String(spread));draw()};
$('zoomin').onclick=()=>setZoom(scale*1.5);$('zoomout').onclick=()=>setZoom(scale/1.5);$('zoomreset').onclick=resetZoom;
$('fullscreen').onclick=()=>{if(document.fullscreenElement)document.exitFullscreen?.();else document.documentElement.requestFullscreen?.()};
addEventListener('keydown',e=>{if(['INPUT','TEXTAREA'].includes(document.activeElement?.tagName))return;if(e.key==='Escape')resetZoom();if(e.key==='+'||e.key==='=')setZoom(scale*1.5);if(e.key==='-')setZoom(scale/1.5);if(e.key==='ArrowRight')move(spreadCount());if(e.key==='ArrowLeft')move(-spreadCount())});
const pointers=new Map();let lastTap=0;
const distance=(a,b)=>Math.hypot(a.x-b.x,a.y-b.y);
stage.addEventListener('pointerdown',e=>{if(e.pointerType==='mouse'&&e.button!==0)return;stage.setPointerCapture?.(e.pointerId);pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===1)gesture={x:e.clientX,y:e.clientY,lastX:e.clientX,lastY:e.clientY,moved:false,pinch:false};if(pointers.size===2){const [a,b]=[...pointers.values()];gesture={pinch:true,dist:distance(a,b),startScale:scale,moved:true}}});
stage.addEventListener('pointermove',e=>{if(!pointers.has(e.pointerId))return;pointers.set(e.pointerId,{x:e.clientX,y:e.clientY});if(pointers.size===2){const [a,b]=[...pointers.values()];if(!gesture?.pinch)gesture={pinch:true,dist:distance(a,b),startScale:scale,moved:true};scale=clamp(gesture.startScale*distance(a,b)/Math.max(1,gesture.dist),1,4);applyZoom();return}if(pointers.size===1&&gesture&&!gesture.pinch){const dx=e.clientX-gesture.lastX,dy=e.clientY-gesture.lastY;if(Math.hypot(e.clientX-gesture.x,e.clientY-gesture.y)>9)gesture.moved=true;if(zoomed()){panX+=dx;panY+=dy;applyZoom()}gesture.lastX=e.clientX;gesture.lastY=e.clientY}});
function endPointer(e){if(!pointers.has(e.pointerId))return;const g=gesture;pointers.delete(e.pointerId);if(pointers.size===0){if(g&&!g.pinch){const dx=e.clientX-g.x,dy=e.clientY-g.y;if(!zoomed()&&Math.abs(dx)>65&&Math.abs(dx)>Math.abs(dy)*1.2)move(dx<0?spreadCount():-spreadCount());else if(!g.moved){const now=Date.now();if(now-lastTap<320){setZoom(zoomed()?1:2.3);lastTap=0}else lastTap=now}}gesture=null}else if(g?.pinch){gesture=null}};
stage.addEventListener('pointerup',endPointer);stage.addEventListener('pointercancel',endPointer);
stage.addEventListener('wheel',e=>{if(!e.ctrlKey&&!e.metaKey)return;e.preventDefault();setZoom(scale*(e.deltaY<0?1.12:.89))},{passive:false});
addEventListener('resize',()=>{if(book)draw()});
if(!catalog[id]){stage.textContent='Book not found';return}
fetch(catalog[id]).then(r=>{if(!r.ok)throw Error('Preview unavailable');return r.json()}).then(data=>{if(!Array.isArray(data.pages)||!data.pages.length)throw Error('No preview pages');book=data;$('book-title').textContent=data.series+' · '+data.title;$('reader-note').textContent=data.status==='published'?'Published edition':data.pages.length+' sequential review pages · Pinch / double-tap to zoom';seek.max=data.pages.length;index=clamp((parseInt(params.get('page'),10)||1)-1,0,data.pages.length-1);draw()}).catch(e=>{stage.textContent=e.message});
})();