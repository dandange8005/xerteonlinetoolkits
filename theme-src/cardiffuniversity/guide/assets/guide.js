// Author guide: copy buttons and the phone-width component menu. The page works without this
// script: the buttons stay hidden and the menu stays open.
(function () {
  "use strict";

  document.querySelectorAll(".g-code-wrap").forEach(function (wrap) {
    var button = wrap.querySelector(".g-copy");
    var code = wrap.querySelector("code");
    if (!button || !code || !navigator.clipboard) return;
    button.hidden = false;
    button.addEventListener("click", function () {
      navigator.clipboard.writeText(code.textContent).then(function () {
        button.textContent = "Copied";
      }, function () {
        button.textContent = "Copy failed: select the code instead";
      });
      window.setTimeout(function () { button.textContent = "Copy"; }, 2000);
    });
  });

  // "On this page": mark the section being read. Without the script the list is plain links.
  var toc = document.querySelector(".g-toc");
  if (toc) {
    var links = [].slice.call(toc.querySelectorAll('a[href^="#"]'));
    var targets = links.map(function (a) { return document.getElementById(a.getAttribute("href").slice(1)); });
    var mark = function () {
      var current = 0;
      targets.forEach(function (target, i) {
        if (target && target.getBoundingClientRect().top <= 120) current = i;
      });
      if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 2) current = links.length - 1;
      links.forEach(function (a, i) {
        if (i === current) a.setAttribute("aria-current", "location");
        else a.removeAttribute("aria-current");
      });
    };
    window.addEventListener("scroll", mark, { passive: true });
    window.addEventListener("resize", mark);
    mark();
  }

  var side = document.querySelector(".g-side");
  if (!side) return;
  var toggle = side.querySelector(".g-side-toggle");
  var list = side.querySelector(".g-side-list");
  var narrow = window.matchMedia("(max-width: 800px)");

  function show(open) {
    toggle.setAttribute("aria-expanded", String(open));
    list.hidden = !open;
  }
  function apply() {
    toggle.hidden = !narrow.matches;
    show(!narrow.matches);
  }
  toggle.addEventListener("click", function () {
    show(toggle.getAttribute("aria-expanded") !== "true");
  });
  narrow.addEventListener("change", apply);
  apply();
})();
