(function(){
  var d=document, root=d.documentElement;
  root.classList.add('js');
  /* always open a page at the top (unless a section anchor is requested) */
  if('scrollRestoration' in history)history.scrollRestoration='manual';
  function toTop(){if(!location.hash||!d.getElementById(location.hash.slice(1))){try{window.scrollTo({top:0,left:0,behavior:'instant'})}catch(e){window.scrollTo(0,0)}}}
  toTop();addEventListener('load',toTop);addEventListener('pageshow',toTop);
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* header state + scroll progress + back-to-top */
  var h=d.querySelector('.site-header'), top=d.querySelector('.to-top'), rp=d.querySelector('.read-progress span');
  function onScroll(){
    var y=window.scrollY, max=d.documentElement.scrollHeight-innerHeight, pct=max>0?(y/max*100):0;
    if(h){h.classList.toggle('is-scrolled',y>30);h.style.setProperty('--scroll',pct+'%');}
    if(top)top.classList.toggle('show',y>700);
    if(rp)rp.style.width=pct+'%';
  }
  addEventListener('scroll',onScroll,{passive:true});onScroll();

  /* mobile nav */
  var b=d.querySelector('.burger'),n=d.getElementById('nav');
  if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o);d.body.style.overflow=o?'hidden':'';});
    n.addEventListener('click',function(e){if(e.target.tagName==='A'){n.classList.remove('open');b.setAttribute('aria-expanded','false');d.body.style.overflow='';}});}

  /* reveal + counters */
  function count(el){
    var to=parseFloat(el.getAttribute('data-count')); if(isNaN(to)||reduce)return;
    var suffix=el.textContent.replace(/[0-9.]/g,''), t0=null, dur=1400;
    function step(t){if(!t0)t0=t;var p=Math.min((t-t0)/dur,1),e=1-Math.pow(1-p,3);el.textContent=Math.round(to*e)+suffix;if(p<1)requestAnimationFrame(step);}
    el.textContent='0'+suffix;requestAnimationFrame(step);
  }
  var els=d.querySelectorAll('.reveal,.step,[data-count]');
  if('IntersectionObserver' in window){
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){
      e.target.classList.add('in');
      if(e.target.hasAttribute('data-count'))count(e.target);
      e.target.querySelectorAll&&e.target.querySelectorAll('[data-count]').forEach(function(c){if(!c.dataset.done){c.dataset.done=1;count(c);}});
      io.unobserve(e.target);}})},{rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){io.observe(e)});
  } else els.forEach(function(e){e.classList.add('in')});

  /* hero rotator */
  var rot=d.querySelector('[data-rotator]');
  if(rot){
    var items=rot.querySelectorAll('.rotator__item'), dots=d.querySelectorAll('.rotator__dots button'), i=0, timer;
    function show(k){i=(k+items.length)%items.length;items.forEach(function(x,j){x.classList.toggle('is-active',j===i)});dots.forEach(function(x,j){x.classList.toggle('is-active',j===i)});}
    function play(){clearInterval(timer);if(!reduce)timer=setInterval(function(){show(i+1)},6000);}
    dots.forEach(function(dt,j){dt.addEventListener('click',function(){show(j);play();})});
    rot.parentNode.addEventListener('mouseenter',function(){clearInterval(timer)});
    rot.parentNode.addEventListener('mouseleave',play);
    play();
  }

  /* practice explorer tabs */
  d.querySelectorAll('[data-explorer]').forEach(function(ex){
    var tabs=[].slice.call(ex.querySelectorAll('[role=tab]'));
    function sel(t,focus){tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;d.getElementById(x.getAttribute('aria-controls')).hidden=!on;});if(focus)t.focus();
      var st_=t.parentNode; if(st_.scrollWidth>st_.clientWidth)st_.scrollLeft=t.offsetLeft-st_.clientWidth/2;}
    tabs.forEach(function(t,k){
      t.addEventListener('click',function(){sel(t)});
      t.addEventListener('keydown',function(e){var m={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(m){e.preventDefault();sel(tabs[(k+m+tabs.length)%tabs.length],true);}});
    });
  });

  /* practice hub */
  d.querySelectorAll('[data-hub]').forEach(function(hub){
    var tabs=[].slice.call(hub.querySelectorAll('[role=tab]')), bar=hub.querySelector('.hub__bar span'), auds=hub.querySelectorAll('.aud'), cur='all';
    function visible(){return tabs.filter(function(t){return !t.classList.contains('is-dim')});}
    function sel(t,focus,noHash){
      tabs.forEach(function(x){var on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;var p=d.getElementById(x.getAttribute('aria-controls'));
        if(on){p.hidden=false;p.style.animation='none';p.offsetHeight;p.style.animation='';}else p.hidden=true;});
      if(bar)bar.style.width=((tabs.indexOf(t)+1)/tabs.length*100)+'%';
      if(focus)t.focus({preventScroll:true});
      var strip=t.parentNode; if(!noHash&&strip.scrollWidth>strip.clientWidth){strip.scrollTo({left:t.offsetLeft-strip.clientWidth/2+t.offsetWidth/2,behavior:reduce?'auto':'smooth'});}
      if(!noHash&&history.replaceState)history.replaceState(null,'','#'+t.dataset.key);
    }
    function step(n){var v=visible(),cur_=tabs.filter(function(t){return t.getAttribute('aria-selected')==='true'})[0],i=v.indexOf(cur_);if(i<0)i=0;sel(v[(i+n+v.length)%v.length],false);}
    tabs.forEach(function(t){
      t.addEventListener('click',function(){sel(t)});
      t.addEventListener('keydown',function(e){var m={ArrowDown:1,ArrowRight:1,ArrowUp:-1,ArrowLeft:-1}[e.key];if(m){e.preventDefault();var v=visible(),i=v.indexOf(t);sel(v[(i+m+v.length)%v.length],true);}});
    });
    hub.querySelectorAll('[data-step]').forEach(function(b){b.addEventListener('click',function(){step(+b.dataset.step)})});
    auds.forEach(function(a){a.addEventListener('click',function(){
      cur=a.dataset.aud;auds.forEach(function(x){var on=x===a;x.classList.toggle('is-active',on);x.setAttribute('aria-pressed',on)});
      tabs.forEach(function(t){t.classList.toggle('is-dim',cur!=='all'&&(' '+t.dataset.aud+' ').indexOf(' '+cur+' ')<0)});
      var selT=tabs.filter(function(t){return t.getAttribute('aria-selected')==='true'})[0];
      if(selT.classList.contains('is-dim'))sel(visible()[0]);
    })});
    var h0=(location.hash||'').slice(1), start=tabs.filter(function(t){return t.dataset.key===h0})[0];
    sel(start||tabs[0],false,true);
  });

  /* testimonial slider */
  d.querySelectorAll('[data-slider]').forEach(function(sl){
    var track=sl.querySelector('.slider__track'), slides=track.children, dots=sl.querySelectorAll('.slider__dots button'), k=0, timer;
    function go(j){k=(j+slides.length)%slides.length;track.style.transform='translateX('+(-100*k)+'%)';dots.forEach(function(x,i){x.classList.toggle('is-active',i===k)});}
    function play(){clearInterval(timer);if(!reduce)timer=setInterval(function(){go(k+1)},8000);}
    sl.querySelector('[data-prev]').addEventListener('click',function(){go(k-1);play()});
    sl.querySelector('[data-next]').addEventListener('click',function(){go(k+1);play()});
    dots.forEach(function(dt,i){dt.addEventListener('click',function(){go(i);play()})});
    var x0=null;track.addEventListener('touchstart',function(e){x0=e.touches[0].clientX},{passive:true});
    track.addEventListener('touchend',function(e){if(x0===null)return;var dx=e.changedTouches[0].clientX-x0;if(Math.abs(dx)>40){go(k+(dx<0?1:-1));play();}x0=null;});
    sl.addEventListener('mouseenter',function(){clearInterval(timer)});sl.addEventListener('mouseleave',play);
    go(0);play();
  });

  /* card spotlight */
  d.querySelectorAll('.card').forEach(function(c){c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect();c.style.setProperty('--mx',(e.clientX-r.left)+'px');c.style.setProperty('--my',(e.clientY-r.top)+'px');});});

  /* insights filter */
  var fs=d.querySelectorAll('.filters button');
  fs.forEach(function(btn){btn.addEventListener('click',function(){
    fs.forEach(function(x){x.setAttribute('aria-pressed','false')});btn.setAttribute('aria-pressed','true');
    var f=btn.getAttribute('data-filter');
    d.querySelectorAll('.posts .post').forEach(function(p){p.hidden=!(f==='all'||p.getAttribute('data-type')===f||p.getAttribute('data-practice')===f);});
  });});

  /* copy email address */
  d.querySelectorAll('[data-copy]').forEach(function(b){b.addEventListener('click',function(){
    var v=b.getAttribute('data-copy'),lbl=b.textContent;
    function done(){b.textContent=b.getAttribute('data-copied');setTimeout(function(){b.textContent=lbl},2200);}
    if(navigator.clipboard){navigator.clipboard.writeText(v).then(done,function(){location.href='mailto:'+v});}else{location.href='mailto:'+v;}
  });});

  /* cookie consent (GDPR): necessary only by default; analytics only after opt-in */
  var w=window,ck=d.getElementById('cookie');
  if(ck){
    var KEY='sm_cookie_consent',MAX=365*864e5,ga=ck.getAttribute('data-ga');
    var opts=d.getElementById('cookie-opts'),an=ck.querySelector('[data-cookie-analytics]');
    var bSet=ck.querySelector('[data-cookie="settings"]'),bSave=ck.querySelector('[data-cookie="save"]');
    function read(){try{var c=JSON.parse(localStorage.getItem(KEY));if(c&&Date.now()-c.t<MAX)return c;}catch(e){}return null;}
    function store(a){var c={a:!!a,t:Date.now(),v:1};try{localStorage.setItem(KEY,JSON.stringify(c));}catch(e){}return c;}
    function loadGA(){
      if(!ga||w.__smGA)return;w.__smGA=1;
      var s=d.createElement('script');s.async=1;s.src='https://www.googletagmanager.com/gtag/js?id='+encodeURIComponent(ga);d.head.appendChild(s);
      w.dataLayer=w.dataLayer||[];w.gtag=function(){w.dataLayer.push(arguments)};
      w.gtag('consent','default',{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'granted'});
      w.gtag('js',new Date());w.gtag('config',ga,{anonymize_ip:true});
    }
    function clearGA(){d.cookie.split(';').forEach(function(c){var n=c.split('=')[0].trim();if(/^_ga/.test(n)){
      var h=location.hostname;['',h,'.'+h,'.'+h.replace(/^www\./,'')].forEach(function(dm){d.cookie=n+'=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/'+(dm?'; domain='+dm:'');});}});}
    function apply(c){if(c.a)loadGA();else clearGA();}
    function show(){var c=read();an.checked=!!(c&&c.a);ck.hidden=false;ck.classList.add('is-open');}
    function hide(){ck.classList.remove('is-open');ck.hidden=true;opts.hidden=true;bSave.hidden=true;bSet.hidden=false;bSet.setAttribute('aria-expanded','false');}
    function choose(a){var c=store(a);var had=w.__smGA;apply(c);hide();if(had&&!a)location.reload();}
    ck.querySelector('[data-cookie="accept"]').addEventListener('click',function(){choose(true)});
    ck.querySelector('[data-cookie="reject"]').addEventListener('click',function(){choose(false)});
    bSave.addEventListener('click',function(){choose(an.checked)});
    bSet.addEventListener('click',function(){opts.hidden=false;bSave.hidden=false;bSet.hidden=true;bSet.setAttribute('aria-expanded','true');an.focus();});
    d.querySelectorAll('[data-cookie-open]').forEach(function(b){b.addEventListener('click',function(){show();opts.hidden=false;bSave.hidden=false;bSet.hidden=true;})});
    var cur=read();if(cur)apply(cur);else show();
  }
})();
