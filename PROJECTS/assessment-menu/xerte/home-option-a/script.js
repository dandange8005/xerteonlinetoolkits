/* ===== Assessment Menu: type search on the Home page =====
   Paste into Project > Optional properties > Script.
   Each row: [type name, category name, page ID, section ID].
   Page and section IDs must match the IDs set in Xerte. */
(function ($) {
  var AM_TYPES = [
    ['In-person, invigilated exam', 'Exams', 'exams', 'in-person-invigilated-exam'],
    ['Open-book exam', 'Exams', 'exams', 'open-book-exam'],
    ['Timed in-class knowledge test', 'Class tests', 'class-tests', 'timed-in-class-knowledge-test'],
    ['Application-based problem test', 'Class tests', 'class-tests', 'application-based-problem-test'],
    ['Mentimeter conceptual understanding check', 'Class tests', 'class-tests', 'mentimeter-conceptual-understanding-check'],
    ['Reflective portfolio', 'Portfolios', 'portfolios', 'reflective-portfolio'],
    ['Annotated bibliography', 'Portfolios', 'portfolios', 'annotated-bibliography'],
    ['Professional portfolio', 'Portfolios', 'portfolios', 'professional-portfolio'],
    ['Artefacts', 'Multimedia assessments', 'multimedia', 'artefacts'],
    ['Posters', 'Multimedia assessments', 'multimedia', 'posters'],
    ['Blog/vlog', 'Multimedia assessments', 'multimedia', 'blog-vlog'],
    ['Assessed seminars', 'Oral and spoken', 'oral', 'assessed-seminars'],
    ['Presentation', 'Oral and spoken', 'oral', 'presentation'],
    ['Viva voce', 'Oral and spoken', 'oral', 'viva-voce'],
    ['OSCEs and ISCEs', 'Practical based', 'practical', 'osces-and-isces'],
    ['Essay', 'Written assessments', 'written', 'essay'],
    ['Report', 'Written assessments', 'written', 'report']
  ];

  function esc(s) { return $('<div/>').text(s).html(); }

  function close($box) {
    $box.find('.am-results').attr('hidden', 'hidden');
    $box.find('input').attr('aria-expanded', 'false');
  }

  // Delegated events: the Home page content is added after this script runs
  $(document).on('input', '.am-search input', function () {
    var $input = $(this), $box = $input.closest('.am-search'), $list = $box.find('.am-results');
    var q = $.trim($input.val()).toLowerCase();
    if (!q) { close($box); return; }
    var html = '';
    $.each(AM_TYPES, function (i, t) {
      if (t[0].toLowerCase().indexOf(q) > -1 || t[1].toLowerCase().indexOf(q) > -1) {
        html += '<li><a href="#' + t[2] + '|' + t[3] + '"><span>' + esc(t[0]) + '</span><span class="am-cat">' + esc(t[1]) + '</span></a></li>';
      }
    });
    $list.html(html || '<li><span class="am-none">No match. <a href="#browse">Browse all types</a></span></li>').removeAttr('hidden');
    $input.attr('aria-expanded', 'true');
  });

  $(document).on('keydown', '.am-search input', function (e) {
    var $box = $(this).closest('.am-search');
    if (e.key === 'Escape') { close($box); }
    if (e.key === 'ArrowDown') {
      var $first = $box.find('.am-results a').first();
      if ($first.length && !$box.find('.am-results').is('[hidden]')) { e.preventDefault(); $first.focus(); }
    }
  });

  $(document).on('keydown', '.am-results a', function (e) {
    var $box = $(this).closest('.am-search'), $links = $box.find('.am-results a'), i = $links.index(this);
    if (e.key === 'ArrowDown' && i < $links.length - 1) { e.preventDefault(); $links.eq(i + 1).focus(); }
    if (e.key === 'ArrowUp') { e.preventDefault(); if (i > 0) { $links.eq(i - 1).focus(); } else { $box.find('input').focus(); } }
    if (e.key === 'Escape') { close($box); $box.find('input').focus(); }
  });

  // Close the list after choosing a result or clicking elsewhere
  $(document).on('click', function (e) {
    $('.am-search').each(function () {
      if (!$.contains(this, e.target) || $(e.target).closest('.am-results a').length) { close($(this)); }
    });
  });
})(jQuery);
