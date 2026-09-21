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

    // Sections carry scroll-margin-top of the same size, so a link lands with the heading exactly
    // GAP below the bar. That puts the spy's threshold precisely on the section's stored offset,
    // and the browser rounding the scroll position down by a fraction of a pixel is enough to
    // leave the previous item highlighted until the reader nudges the page. A few pixels of slack
    // keeps the clicked section selected on arrival.
    var SLACK = 8;

    // The player makes one of two elements sticky, depending on where the author put the page
    // menu: #topnav itself when it sits above the header, or the #pageLinks wrapper it is moved
    // into when the author sets navbarPos=below (application.js). Measure whichever one is
    // actually sticky, not just #topnav, which is left static in the second case.
    function stickyNav() {
        var candidates = [document.getElementById('pageLinks'), document.getElementById('topnav')];
        for (var i = 0; i < candidates.length; i++) {
            var el = candidates[i];
            if (!el || el.offsetHeight === 0) {
                continue;
            }
            var position = window.getComputedStyle(el).position;
            if (position === 'sticky' || position === 'fixed') {
                return el;
            }
        }
        return null; // the bar scrolls away with the page, so there is nothing to clear
    }

    function stickyNavHeight() {
        var el = stickyNav();
        return el ? Math.round(el.getBoundingClientRect().height) : 0;
    }

    function apply() {
        var height = stickyNavHeight();
        document.documentElement.style.setProperty('--cu-sticky-nav', height + 'px');

        // A project with more than ten pages gets an inline `top: 65px` on the affixed section
        // menu (application.js), and an inline style beats the stylesheet. Set our own inline
        // value so the menu clears the bar whatever the project's size.
        var menu = document.querySelector('.bs-docs-sidenav');
        if (menu) {
            if (height) {
                menu.style.top = (height + GAP + 8) + 'px';
                menu.setAttribute('data-cu-top', 'set');
            } else if (menu.getAttribute('data-cu-top')) {
                menu.style.top = '';
                menu.removeAttribute('data-cu-top');
            }
        }

        var $ = window.jQuery;
        if (!$) {
            return;
        }
        var spy = $('body').data('scrollspy');
        if (spy && spy.options) {
            spy.options.offset = height + GAP + SLACK;
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

    // A host or a test can force a recalculation after changing the layout.
    window.cardiffuniV3 = { apply: apply };
})();
