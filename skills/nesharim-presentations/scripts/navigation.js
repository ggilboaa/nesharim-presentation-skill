(function(){
  if(window.__nesharimNavInit)return;
  var panel=document.querySelector('.controls');if(!panel)return;
  window.__nesharimNavInit=true;
  var timer=null,mouseOnPanel=false;
  function hide(){timer=null;if(!mouseOnPanel)document.body.classList.remove('nav-visible')}
  function reveal(autoHide){clearTimeout(timer);document.body.classList.add('nav-visible');if(autoHide&&!mouseOnPanel)timer=setTimeout(hide,2200)}
  function deferHide(){clearTimeout(timer);timer=setTimeout(hide,650)}
  document.addEventListener('pointermove',function(e){if(e.pointerType==='touch')return;if(e.clientY>=innerHeight-90)reveal(false);else if(timer===null)deferHide()});
  document.addEventListener('pointerleave',deferHide);
  panel.addEventListener('pointerenter',function(e){if(e.pointerType==='touch')return;mouseOnPanel=true;reveal(false)});
  panel.addEventListener('pointerleave',function(e){if(e.pointerType==='touch')return;mouseOnPanel=false;deferHide()});
  document.addEventListener('pointerup',function(e){if(e.pointerType==='touch')reveal(true)});
  document.addEventListener('keydown',function(e){if(['ArrowLeft','ArrowRight','PageDown','PageUp','Home','End',' ','Tab'].includes(e.key))reveal(true)});
  panel.addEventListener('focusin',function(){reveal(true)});
  var fs=document.querySelector('#fs');
  function label(){if(!fs)return;var s=document.fullscreenElement?'יציאה ממסך מלא':'מסך מלא';fs.setAttribute('aria-label',s);fs.title=s}
  document.addEventListener('fullscreenchange',function(){label();reveal(true)});label();
})();
