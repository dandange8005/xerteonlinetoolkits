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

    // A link to a section jumps before the images above it have finished loading. They then push
    // the target down, leaving the page short of it - far enough on an image-heavy page to leave
    // the section menu highlighting a section or two earlier. Keep putting the target where it
    // belongs until the layout stops moving, and stop the moment the reader scrolls themselves.
    var attemptsLeft = 0;
    var targetTimer = null;
    var readerMoved = false;

    function wantedScrollTop(target) {
        var top = window.pageYOffset + target.getBoundingClientRect().top;
        return Math.max(0, Math.round(top - (stickyNavHeight() + GAP)));
    }

    function settleOnTarget() {
        var id = window.location.hash.slice(1);
        var target = id ? document.getElementById(id) : null;
        if (!target || !target.offsetHeight) {
            return;
        }
        var wanted = wantedScrollTop(target);
        if (Math.abs(window.pageYOffset - wanted) > 2) {
            // This theme does not scroll smoothly, but a host might: both scrollTo() and its
            // 'auto' behaviour defer to the CSS, and an animated correction never arrives before
            // the next attempt restarts it. Turn smoothing off for this one jump.
            var scroller = document.scrollingElement || document.documentElement;
            var previous = scroller.style.scrollBehavior;
            scroller.style.scrollBehavior = 'auto';
            window.scrollTo(0, wanted);
            scroller.style.scrollBehavior = previous;
        }
        apply();
    }

    function tick() {
        if (readerMoved || attemptsLeft <= 0) {
            return;
        }
        attemptsLeft -= 1;
        settleOnTarget();
        targetTimer = window.setTimeout(tick, 200);
    }

    function startSettling() {
        readerMoved = false;
        attemptsLeft = 25; // about five seconds, long enough for a page of screenshots to load
        window.clearTimeout(targetTimer);
        tick();
    }

    // Any of these means the reader has taken over, so stop moving the page under them. None of
    // them fire for a programmatic scroll, so no guard is needed. mousedown covers dragging the
    // scrollbar, which the others miss.
    function readerTookOver() {
        readerMoved = true;
        window.clearTimeout(targetTimer);
    }

    window.addEventListener('wheel', readerTookOver, { passive: true });
    window.addEventListener('touchstart', readerTookOver, { passive: true });
    window.addEventListener('mousedown', readerTookOver, { passive: true });
    window.addEventListener('keydown', readerTookOver);

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
    window.addEventListener('load', function () {
        schedule();
        startSettling(); // a link followed on load lands properly once the images are in
    });
    window.addEventListener('resize', schedule);

    // The player renders each page asynchronously and announces it, and it moves between pages
    // with pushState, which fires no hashchange. Without this the measurement can sit at 0px for
    // a whole page.
    var playerEvents = window.jQuery && window.jQuery(document);
    if (playerEvents && typeof playerEvents.on === 'function') {
        playerEvents.on('contentLoaded', function () {
            schedule();
            startSettling();
        });
    }

    // Opening the collapsed page menu makes the bar taller without resizing the window.
    if (window.ResizeObserver) {
        var observer = new window.ResizeObserver(schedule);
        ['topnav', 'pageLinks'].forEach(function (id) {
            var el = document.getElementById(id);
            if (el) {
                observer.observe(el);
            }
        });
    }
    window.addEventListener('hashchange', function () {
        schedule();       // the player swaps pages without reloading
        startSettling();
    });

    // A host or a test can force a recalculation after changing the layout.
    window.cardiffuniV3 = {
        apply: apply,
        settleOnTarget: settleOnTarget,
        startSettling: startSettling,
        // for the theme's checks: is the script still trying to land on a target?
        state: function () { return { settling: attemptsLeft > 0 && !readerMoved, readerMoved: readerMoved }; }
    };
})();
