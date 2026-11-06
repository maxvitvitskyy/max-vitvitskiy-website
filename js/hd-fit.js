/* Catalog intro on desktop: the first line of the text lines up with the top of the heading letters and the last line with the heading's baseline. */
(function(){
  var hd=document.querySelector('.hd');
  if(!hd)return;
  var h=hd.querySelector('h1'),p=hd.querySelector('p');
  if(!h||!p)return;
  var cv=document.createElement('canvas').getContext('2d');
  var wide=matchMedia('(min-width:1100px)');

  function metrics(el,txt){
    var cs=getComputedStyle(el);
    cv.font=cs.fontStyle+' '+cs.fontWeight+' '+cs.fontSize+' '+cs.fontFamily;
    var m=cv.measureText(txt);
    return {cap:m.actualBoundingBoxAscent,asc:m.fontBoundingBoxAscent};
  }
  function lines(){
    var r=document.createRange();r.selectNodeContents(p);
    var t=[];[].forEach.call(r.getClientRects(),function(q){if(q.width<1)return;var y=Math.round(q.top);if(t.indexOf(y)<0)t.push(y)});
    return t.sort(function(a,b){return a-b});
  }
  function reset(){p.style.fontSize='';p.style.lineHeight='';p.style.position='';p.style.top='';p.style.paddingBottom=''}

  function fit(){
    reset();
    if(!wide.matches)return;
    /* heading metrics from a plain clone: unaffected by the entrance animation */
    var c=document.createElement('h1');
    c.innerHTML=h.textContent.replace(/\s+/g,' ').trim().replace(/^(\S+)\s(.*)$/,'$1 <i>$2</i>');
    c.style.cssText='position:absolute;visibility:hidden;margin:0;left:0;top:0';
    hd.appendChild(c);
    c.insertAdjacentHTML('beforeend','<span style="display:inline-block;width:0;height:0"></span>');
    var word=c.querySelector('i')||c;
    var hm=metrics(word,'БТИ');
    var hTop=h.getBoundingClientRect().top;
    var hBase=hTop+(c.lastChild.getBoundingClientRect().bottom-c.getBoundingClientRect().top);
    var hOff=hBase-hTop;
    hd.removeChild(c);

    p.style.paddingBottom='0';
    var best=null;
    for(var s=17;s>=12;s-=.25){
      p.style.fontSize=s+'px';p.style.lineHeight='1.6';
      var n=lines().length;
      if(n<2)continue;
      var pm=metrics(p,'Я');
      var L=(hm.cap-pm.cap)/(n-1);
      if(L>=1.45*s&&L<=1.95*s){best={s:s,L:L,n:n};break}
    }
    if(!best){reset();return}
    p.style.fontSize=best.s+'px';p.style.lineHeight=best.L+'px';
    var pm2=metrics(p,'Я');
    /* layout coordinates (offsetTop) ignore the entrance transforms that may still be running */
    var r=document.createRange();r.selectNodeContents(p);
    var firstTop=Infinity;[].forEach.call(r.getClientRects(),function(q){if(q.width>=1&&q.top<firstTop)firstTop=q.top});
    var pBase=p.offsetTop+(firstTop-p.getBoundingClientRect().top)+pm2.asc;
    var hCapTop=h.offsetTop+hOff-hm.cap;
    var dy=hCapTop-(pBase-pm2.cap);
    p.style.position='relative';p.style.top=dy+'px';
  }

  var t;
  function later(){clearTimeout(t);t=setTimeout(fit,100)}
  addEventListener('resize',later);
  if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);
  addEventListener('load',fit,{once:true});
  fit();
})();
