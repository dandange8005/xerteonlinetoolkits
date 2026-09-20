/**
 * Cardiff University Theme v3 - theme script
 *
 * The Xerte site player loads <theme>/<theme>.js automatically (application.js, cssSetUp).
 * This file exists for the two things the stylesheet cannot know on its own: how tall the
 * sticky page menu is, and where the section menu's scroll spy should switch.
 *
 * 1. Publishes the sticky navbar's height as --cu-sticky-nav on <html>. The stylesheet uses
 *    it to hold the affixed section menu clear of the bar and to set scroll-margin on
 *    sections. The value is 0px whenever the navbar is not sticky.
 * 2. Gives Bootstrap's scroll spy the same offset, so the section menu highlights the
 *    section whose heading is visible below the bar rather than the one hidden behind it.
 *
 * No dependencies beyond what the player already loads. Safe when the elements are absent.
 */
(function () {
    'use strict';

    var GAP = 16; // --cu-space-4: breathing room below the bar

    function stickyNavHeight() {
        var nav = document.getElementById('topnav');
        if (!nav || !nav.offsetParent && nav.offsetHeight === 0) {
            return 0;
        }
        var position = window.getComputedStyle(nav).position;
        if (position !== 'sticky' && position !== 'fixed') {
            return 0; // the bar scrolls away with the page, so nothing to clear
        }
        return Math.round(nav.getBoundingClientRect().height);
    }

    function apply() {
        var height = stickyNavHeight();
        document.documentElement.style.setProperty('--cu-sticky-nav', height + 'px');

        var $ = window.jQuery;
        if (!$) {
            return;
        }
        var spy = $('body').data('scrollspy');
        if (spy && spy.options) {
            spy.options.offset = height + GAP;
            if (typeof spy.refresh === 'function') {
                spy.refresh();
            }
            if (typeof spy.process === 'function') {
                spy.process();
            }
        }
    }

    var pending = null;
    function schedule() {
        window.clearTimeout(pending);
        pending = window.setTimeout(apply, 150);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', schedule);
    } else {
        schedule();
    }
    window.addEventListener('load', schedule);
    window.addEventListener('resize', schedule);
    window.addEventListener('hashchange', schedule); // the player swaps pages without reloading
})();
