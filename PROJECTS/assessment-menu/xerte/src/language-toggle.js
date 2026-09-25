/* Language link: puts a link to the other-language Xerte project in the page header.
   The English project links to the Welsh one. In the Welsh project set label to 'English' and lang to 'en-GB'.
   Styled by the theme's #language-toggle. Nothing is added until the URL is set. */
(function () {
  var OTHER_PROJECT = { url: '', label: 'Cymraeg', lang: 'cy' }; // url: the play link of the Welsh project, when it exists
  var url = window.AM_LANGUAGE_URL || OTHER_PROJECT.url; // AM_LANGUAGE_URL lets local-preview.html test the link

  function add() {
    var header = document.getElementById('overview');
    if (!url || !header) { return false; }
    if (document.getElementById('language-toggle')) { return true; }
    var link = document.createElement('a');
    link.id = 'language-toggle';
    link.href = url;
    link.lang = OTHER_PROJECT.lang;
    link.setAttribute('hreflang', OTHER_PROJECT.lang);
    link.innerHTML = '<i class="fa-solid fa-language" aria-hidden="true"></i><span class="language-toggle-text"></span>';
    link.lastChild.textContent = OTHER_PROJECT.label;
    header.insertBefore(link, header.firstChild);
    return true;
  }

  // The project script runs before the player has built the page, so retry briefly.
  var tries = 0;
  (function wait() {
    if (!add() && url && tries++ < 50) { setTimeout(wait, 100); }
  })();
})();
