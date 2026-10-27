// Uncovers the hero engraving from the summit down while its sticky stage is pinned.
// Sets --reveal (0 to 1) on .scroll-hero; the CSS mask reads it.
(function () {
  var hero = document.querySelector('.scroll-hero');
  if (!hero) return;
  var stage = hero.querySelector('.scroll-hero-stage');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
  var queued = false;
  var START = 0;   // share of the picture already showing at the top of the page

  function update() {
    queued = false;
    var travel = hero.offsetHeight - stage.offsetHeight;
    var p;
    // No scrolling room (very tall window, e.g. a full-page screenshot) or reduced motion: show it all.
    if (reduce.matches || travel <= 0 || window.innerHeight >= hero.offsetHeight) {
      p = 1;
    } else {
      p = -hero.getBoundingClientRect().top / (travel * 0.8);
      p = Math.min(1, Math.max(0, p));
      p = 1 - Math.pow(1 - p, 2);
    }
    hero.style.setProperty('--reveal', (START + (1 - START) * p).toFixed(3));
  }

  function request() {
    if (!queued) { queued = true; requestAnimationFrame(update); }
  }

  hero.style.setProperty('--reveal', String(START));
  window.addEventListener('scroll', request, { passive: true });
  window.addEventListener('resize', request);
  update();
})();
