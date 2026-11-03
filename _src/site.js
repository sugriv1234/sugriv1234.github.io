(function () {
  var d = document;

  /* Abidjan local time (GMT+0) */
  var clk = d.querySelector('[data-clock]');
  function tick() {
    if (!clk) return;
    var n = new Date();
    clk.textContent = ('0' + n.getUTCHours()).slice(-2) + ':' + ('0' + n.getUTCMinutes()).slice(-2);
  }
  tick(); setInterval(tick, 20000);

  /* active anchor in the section bar */
  var links = [].slice.call(d.querySelectorAll('.an a[data-sec]'));
  var bar = d.querySelector('.an-in');
  if ('IntersectionObserver' in window && links.length) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) {
          var on = a.getAttribute('data-sec') === en.target.id;
          a.classList.toggle('on', on);
          if (on && bar) bar.scrollTo({ left: a.offsetLeft - 16, behavior: 'smooth' });
        });
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    links.forEach(function (a) { var s = d.getElementById(a.getAttribute('data-sec')); if (s) io.observe(s); });

    /* reveal on scroll */
    var rv = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in'); rv.unobserve(en.target); } });
    }, { rootMargin: '0px 0px -8% 0px' });
    [].forEach.call(d.querySelectorAll('.rv'), function (el) { rv.observe(el); });
  } else {
    [].forEach.call(d.querySelectorAll('.rv'), function (el) { el.classList.add('in'); });
  }

  /* search */
  var box = d.querySelector('.sr'), inp = box && box.querySelector('input'), res = box && box.querySelector('.sr-res');
  var idx = [];
  try { idx = JSON.parse(d.getElementById('sidx').textContent); } catch (e) {}
  var norm = function (s) { return (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); };
  idx.forEach(function (it) { it.n = norm(it.t + ' ' + it.s + ' ' + it.d); });
  var last = null;

  function render(q) {
    q = norm(q.trim());
    res.innerHTML = '';
    if (!q) return;
    var terms = q.split(/\s+/);
    var hits = idx.filter(function (it) { return terms.every(function (t) { return it.n.indexOf(t) > -1; }); }).slice(0, 12);
    if (!hits.length) { res.innerHTML = '<li class="sr-none">' + (window.UI && UI.none || '—') + '</li>'; return; }
    hits.forEach(function (it, i) {
      var li = d.createElement('li');
      var a = d.createElement('a');
      a.href = it.h; a.setAttribute('role', 'option');
      if (/^https?:/.test(it.h)) { a.target = '_blank'; a.rel = 'noopener'; }
      var s = d.createElement('span'); s.className = 'mono'; s.textContent = it.s;
      var t = d.createElement('span'); t.className = 'sr-t'; t.textContent = it.t;
      a.appendChild(s); a.appendChild(t);
      a.addEventListener('click', close);
      li.appendChild(a); res.appendChild(li);
    });
  }
  function open() {
    if (!box) return;
    last = d.activeElement;
    box.hidden = false; d.body.classList.add('noscroll');
    setTimeout(function () { inp.focus(); }, 30);
  }
  function close() {
    if (!box || box.hidden) return;
    box.hidden = true; d.body.classList.remove('noscroll');
    if (last && last.focus) last.focus();
  }
  [].forEach.call(d.querySelectorAll('[data-open-search]'), function (b) { b.addEventListener('click', open); });
  if (box) {
    box.querySelector('[data-close-search]').addEventListener('click', close);
    box.addEventListener('click', function (ev) { if (ev.target === box) close(); });
    inp.addEventListener('input', function () { render(inp.value); });
    inp.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter') { var f = res.querySelector('a'); if (f) f.click(); }
      if (ev.key === 'ArrowDown') { var f2 = res.querySelector('a'); if (f2) { ev.preventDefault(); f2.focus(); } }
    });
    res.addEventListener('keydown', function (ev) {
      var a = d.activeElement; if (!a || a.tagName !== 'A') return;
      var li = a.parentNode;
      if (ev.key === 'ArrowDown' && li.nextElementSibling) { ev.preventDefault(); li.nextElementSibling.firstChild.focus(); }
      if (ev.key === 'ArrowUp') { ev.preventDefault(); (li.previousElementSibling ? li.previousElementSibling.firstChild : inp).focus(); }
    });
  }
  d.addEventListener('keydown', function (ev) {
    if (ev.key === 'Escape') close();
    var tag = (d.activeElement && d.activeElement.tagName) || '';
    if ((ev.key === '/' || ((ev.metaKey || ev.ctrlKey) && ev.key.toLowerCase() === 'k')) && !/INPUT|TEXTAREA/.test(tag)) { ev.preventDefault(); open(); }
  });
})();
