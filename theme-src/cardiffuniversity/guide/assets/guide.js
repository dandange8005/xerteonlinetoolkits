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
