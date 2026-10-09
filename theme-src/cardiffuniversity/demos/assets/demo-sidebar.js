/* The player pins the section menu with Bootstrap's affix plugin (application.js). The demo pages load
   Bootstrap but not the player's script, so this does the same job for them. The menu is pinned once
   the page has scrolled to where it starts, less the gap the theme leaves above a pinned menu. */
jQuery(function ($) {
    var $menu = $('.bs-docs-sidenav');
    if (!$menu.length || !$.fn.affix) { return; }
    $menu.affix({
        offset: {
            top: function () {
                // Measured with the menu in its resting place, so the number stays right when the page reflows.
                return $menu.parent().offset().top + parseFloat($menu.css('margin-top') || 0) - 24;
            }
        }
    });
});
