/* Catalog motion: entrance choreography, scroll reveal for cards, soft exit for browsers without cross-document view transitions.
   Everything is progressive: without JS, GSAP or with prefers-reduced-motion the page is simply shown. */
(function(){
  var root=document.documentElement;
  var wall=document.querySelector('.wall');
  if(!wall)return;
  var cards=[].slice.call(wall.querySelectorAll('.w'));
  var running=[];
  var started=false;

  function showAll(){
    root.classList.add('hero-in');
    cards.forEach(function(c){c.classList.add('rv-done')});
  }

  /* ---- reveal one batch of cards (staggered by position in the batch) ---- */
  function reveal(batch){
    batch.forEach(function(c,i){
      if(c.classList.contains('rv-done'))return;
      var img=c.querySelector('.ph img:not(.alt)'),cap=c.querySelector('.cap');
      var d=Math.min(i,8)*.085;
      c.classList.add('rv-busy');
      gsap.set(c,{opacity:0,y:48});
      if(img)gsap.set(img,{scale:1.16});
      if(cap)gsap.set(cap,{opacity:0,y:14});
      c.classList.add('rv-done');
      var tl=gsap.timeline({delay:d,onComplete:function(){
        gsap.set([c,img,cap].filter(Boolean),{clearProps:'opacity,transform,scale'});
        requestAnimationFrame(function(){requestAnimationFrame(function(){c.classList.remove('rv-busy')})});
        var k=running.indexOf(tl);if(k>-1)running.splice(k,1);
      }});
      tl.to(c,{opacity:1,y:0,duration:1.05,ease:'power3.out'},0);
      if(img)tl.to(img,{scale:1,duration:1.7,ease:'expo.out'},0);
      if(cap)tl.to(cap,{opacity:1,y:0,duration:.85,ease:'power2.out'},.3);
      running.push(tl);
    });
  }

  /* called before any filter change: finish every running reveal and unhide the rest (Flip animates them from here) */
  function finish(){
    running.slice().forEach(function(t){t.progress(1)});
    cards.forEach(function(c){
      if(!c.classList.contains('rv-done')){c.classList.add('rv-done')}
    });
  }
  window.catalogMotion={finish:finish};

  if(!window.gsap||!root.classList.contains('js')){showAll();return}

  /* ---- entrance ---- */
  function splitTitle(h){
    if(h.dataset.split)return h.querySelectorAll('.wd>span');
    h.dataset.split='1';
    var parts=[].slice.call(h.childNodes),html='';
    parts.forEach(function(n){
      if(n.nodeType===3){n.textContent.split(/\s+/).filter(Boolean).forEach(function(w){html+='<span class="wd"><span>'+w+'</span></span> '})}
      else html+='<span class="wd"><span>'+n.outerHTML+'</span></span> ';
    });
    h.innerHTML=html.trim();
    h.setAttribute('aria-label',h.textContent);
    return h.querySelectorAll('.wd>span');
  }

  function start(){
    if(started)return;started=true;
    var words=splitTitle(document.querySelector('.hd h1'));
    var chips=[].slice.call(document.querySelectorAll('.filters button'));
    gsap.set(words,{yPercent:115});
    gsap.set(['.top .logo','.top .lng','.top .back','.hd .k','.hd p'],{opacity:0});
    gsap.set(chips,{opacity:0,y:14});
    root.classList.add('hero-in');

    var tl=gsap.timeline({defaults:{ease:'power3.out'}});
    tl.to('.top .logo',{opacity:1,duration:.9},0)
      .fromTo('.top .lng',{x:14},{opacity:1,x:0,duration:.9},.08)
      .fromTo('.top .back',{x:14},{opacity:1,x:0,duration:.9},.08)
      .fromTo('.hd .k',{y:14},{opacity:1,y:0,duration:.8},.2)
      .to(words,{yPercent:0,duration:1.25,ease:'expo.out',stagger:.13},.3)
      .fromTo('.hd p',{y:18},{opacity:1,y:0,duration:1,ease:'power2.out'},.75)
      .to(chips,{opacity:1,y:0,duration:.8,stagger:.05,ease:'power2.out'},.9)
      .call(observe,null,.85)
      .add(function(){
        gsap.set(['.top .logo','.top .lng','.top .back','.hd .k','.hd p'].concat(chips),{clearProps:'opacity,transform'});
        gsap.set(words,{clearProps:'transform'});
      });
  }

  /* ---- scroll reveal ---- */
  var io=null;
  function observe(){
    if(!('IntersectionObserver' in window)){cards.forEach(function(c){c.classList.add('rv-done')});return}
    io=new IntersectionObserver(function(entries){
      var vis=entries.filter(function(e){return e.isIntersecting}).map(function(e){return e.target});
      if(!vis.length)return;
      vis.sort(function(a,b){return cards.indexOf(a)-cards.indexOf(b)});
      vis.forEach(function(c){io.unobserve(c)});
      reveal(vis);
    },{rootMargin:'0px 0px -7% 0px',threshold:.08});
    cards.forEach(function(c){if(!c.classList.contains('rv-done'))io.observe(c)});
  }

  /* start once fonts are in (the title is measured by its words), but never wait long */
  var go=function(){start()};
  if(document.fonts&&document.fonts.ready){document.fonts.ready.then(go);setTimeout(go,1200)}else go();
  setTimeout(function(){if(!started)showAll()},3500);

  /* page restored from the back/forward cache: show it as is */
  addEventListener('pageshow',function(e){if(e.persisted){root.classList.remove('leaving');showAll()}});
})();
