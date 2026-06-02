const b=new Date(1994,10,2),t=new Date();
const age=t.getFullYear()-b.getFullYear()-(t<b.setFullYear(t.getFullYear()));
var ageEl=document.getElementById("age");if(ageEl)ageEl.textContent=age;

(function(){
  var html=document.documentElement;
  var btn=document.getElementById('theme-toggle');
  var iconOff=document.getElementById('icon-off');
  var iconOn=document.getElementById('icon-on');
  function isDark(){
    var saved=localStorage.getItem('theme');
    if(saved)return saved==='dark';
    return window.matchMedia('(prefers-color-scheme:dark)').matches;
  }
  function apply(dark){
    html.setAttribute('data-theme',dark?'dark':'light');
    iconOff.style.display=dark?'none':'';
    iconOn.style.display=dark?'':'none';
  }
  apply(isDark());
  btn.addEventListener('click',function(){
    var dark=!isDark();
    localStorage.setItem('theme',dark?'dark':'light');
    apply(dark);
  });
})();
