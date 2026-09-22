#!/usr/bin/env python3
"""Computed-style checks for the cardiffuni-v3 theme (headless Chrome, standard library only).

Usage (from the theme folder):
    python3 tests/check_theme.py              run every group
    python3 tests/check_theme.py tokens roles run the named groups only
Exit code 1 if any selected check fails.
"""
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURE = HERE / "fixture.html"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

# A check may name a variant as a fifth element: the fixture is then rendered with that header
# markup and window width (headless Chrome will not go below about 485px). Names must be unique.
PARTNER_LOGO = ("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='60'"
                "%3E%3Crect width='160' height='60' fill='%23666'/%3E%3C/svg%3E")  # an uploaded logo has a size


def header_markup(left, right):
    """The player's header with the left logo, the right logo or both switched on."""
    def slot(side, src, on):
        img = f'<img class="logo logo{side} themeLogo" src="{src}" alt="Logo {side}">' if on else ""
        return f'<div class="logo{side}"' + ("" if on else ' style="display:none"') + f">{img}</div>"
    cls = "jumbotron" + (" logoL" if left else "") + (" logoR" if right else "")
    return (f'<header class="{cls}" id="overview"><div class="container">'
            + slot("L", "../logo_left.svg", left) + slot("R", PARTNER_LOGO, right)
            + '<div class="titles"><h1 id="pageTitle">Assessment Menu</h1>'
              '<p id="pageSubTitle">Designing meaningful, inclusive and future-focused assessment</p></div>'
              "</div></header>")


VARIANTS = {
    f"{name} {width}px": (width, header_markup(*logos))
    for name, logos in (("right logo", (False, True)), ("both logos", (True, True)))
    for width in (1280, 800, 485)
}

# (group, name, JavaScript expression evaluated in the fixture, expected string[, variant])
CHECKS = [
    ("smoke", "theme loaded: body copy is 18px", "cs('body','fontSize')", "18px"),
    ("tokens", "--cu-action is dark Cardiff red", "v('var(--cu-action)')", "rgb(194, 31, 22)"),
    ("tokens", "--cu-callout-tip is Cadet", "v('var(--cu-callout-tip)')", "rgb(94, 185, 155)"),
    ("tokens", "--cu-space-6 is 24px", "v('var(--cu-space-6)','paddingTop')", "24px"),
    ("roles", "action unchanged: #C21F16", "v('var(--color-action)')", "rgb(194, 31, 22)"),
    ("roles", "action hover unchanged: #A11A12", "v('var(--color-action-hover)')", "rgb(161, 26, 18)"),
    ("roles", "error is #A11A12", "v('var(--color-status-error)')", "rgb(161, 26, 18)"),
    ("roles", "focus is black", "v('var(--color-focus)')", "rgb(18, 18, 18)"),
    ("roles", "draft label text is black", "v('var(--color-draft)')", "rgb(18, 18, 18)"),
    ("roles", "draft label background is Yellow", "v('var(--color-draft-bg)','backgroundColor')", "rgb(255, 179, 0)"),
    ("roles", "tertiary text is grey-70", "v('var(--color-text-tertiary)')", "rgb(102, 102, 102)"),
    ("roles", "link blue unchanged", "v('var(--color-link-default)')", "rgb(4, 91, 198)"),
    ("roles", "brand red unchanged", "v('var(--color-brand-primary)')", "rgb(228, 37, 27)"),
    ("roles", "heading font is the Franklin Gothic stack", "cs('#pageTitle','fontFamily').split(',')[0].trim()", '"Franklin Gothic Heavy"'),
    # --color-light is the off-white for soft backgrounds (v2's #f9fafb); the page itself stays white.
    ("roles", "light is an off-white: lighter than the surface grey, not white",
     "(function(){var c=rgbOf(v('var(--color-light)','backgroundColor'));return String(c[0]<254.5&&c[0]>242.5)})()", "true"),
    ("roles", "light is neutral, with no colour tint",
     "(function(){var c=rgbOf(v('var(--color-light)','backgroundColor'));return String(Math.abs(c[0]-c[1])<0.5&&Math.abs(c[1]-c[2])<0.5)})()", "true"),
    ("roles", "the page background is white", "cs('body','backgroundColor')", "rgb(255, 255, 255)"),
    ("roles", "primary button still dark red", "cs('.button.button-primary','backgroundColor')", "rgb(194, 31, 22)"),
    ("rules", "rule is 1px", "cs('#rule','borderTopWidth')", "1px"),
    ("rules", "rule is neutral grey-30", "cs('#rule','borderTopColor')", "rgb(204, 204, 204)"),
    ("rules", "strong rule is 2px", "cs('#rule-strong','borderTopWidth')", "2px"),
    ("rules", "strong rule is ink", "cs('#rule-strong','borderTopColor')", "rgb(18, 18, 18)"),
    ("rules", "rule has 32px space above", "cs('#rule','marginTop')", "32px"),
    ("callouts", "grey surface", "cs('#callout-tip','backgroundColor')", "rgb(242, 242, 242)"),
    ("callouts", "4px left rule", "cs('#callout-tip','borderLeftWidth')", "4px"),
    ("callouts", "tip rule is Cadet", "cs('#callout-tip','borderLeftColor')", "rgb(94, 185, 155)"),
    ("callouts", "tip disc is Cadet", "cs('#callout-tip .fa-stack-2x','color')", "rgb(94, 185, 155)"),
    ("callouts", "tip glyph is black", "cs('#callout-tip .fa-stack-1x','color')", "rgb(18, 18, 18)"),
    ("callouts", "no modifier = key point, black rule", "cs('#callout-key','borderLeftColor')", "rgb(18, 18, 18)"),
    ("callouts", "key point glyph is white", "cs('#callout-key .fa-stack-1x','color')", "rgb(255, 255, 255)"),
    ("callouts", "warning rule is brand red", "cs('#callout-warning','borderLeftColor')", "rgb(228, 37, 27)"),
    ("callouts", "good practice rule is Forest Green", "cs('#callout-good','borderLeftColor')", "rgb(7, 135, 62)"),
    ("callouts", "title is bold", "cs('#callout-tip .cu-callout-title','fontWeight')", "700"),
    ("callouts", "icon and text sit in a grid", "cs('#callout-tip','display')", "grid"),
    ("callouts", "square corners", "cs('#callout-tip','borderTopLeftRadius')", "0px"),
    ("callouts", "old v2 callout no longer styled", "cs('#old-callout','borderLeftWidth')", "0px"),
    ("callouts", "simple markup: disc drawn in CSS, tip colour", "ps('#callout-tip-simple','::before','backgroundColor')", "rgb(94, 185, 155)"),
    ("callouts", "simple markup: glyph colour on the disc", "ps('#callout-tip-simple','::before','color')", "rgb(18, 18, 18)"),
    ("callouts", "simple markup: disc is 28px", "ps('#callout-tip-simple','::before','width')", "28px"),
    ("callouts", "simple markup: no modifier = key point, black disc", "ps('#callout-key-simple','::before','backgroundColor')", "rgb(18, 18, 18)"),
    ("callouts", "authored fa-stack markup draws no CSS disc", "ps('#callout-tip','::before','content')", "none"),
    ("callouts", "both markup forms align their titles at the same x",
     "(function(){var a=document.querySelector('#callout-tip .cu-callout-title').getBoundingClientRect(),"
     "b=document.querySelector('#callout-tip-simple .cu-callout-title').getBoundingClientRect();"
     "return String(Math.abs(a.left-b.left)<=0.5)})()", "true"),
    ("callouts", "simple markup: disc centred on the title line (within 1px)",
     "(function(){var c=document.querySelector('#callout-tip-simple'),s=getComputedStyle(c,'::before'),"
     "r=c.getBoundingClientRect(),t=c.querySelector('.cu-callout-title').getBoundingClientRect();"
     "var top=r.top+parseFloat(getComputedStyle(c).paddingTop);"
     "return String(Math.abs((top+parseFloat(s.height)/2)-(t.top+t.height/2))<=1)})()", "true"),
    ("callouts", "icon disc centred on the title's first line (within 1px)",
     "(function(){var i=document.querySelector('#callout-tip .cu-callout-icon').getBoundingClientRect(),"
     "t=document.querySelector('#callout-tip .cu-callout-title').getBoundingClientRect();"
     "return String(Math.abs((i.top+i.height/2)-(t.top+t.height/2))<=1)})()", "true"),
    ("header", "white background", "cs('#overview','backgroundColor')", "rgb(255, 255, 255)"),
    ("header", "no gradient", "cs('#overview','backgroundImage')", "none"),
    ("header", "no overlay", "ps('#overview','::before','content')", "none"),
    ("header", "red top edge is 4px", "cs('#overview','borderTopWidth')", "4px"),
    ("header", "red top edge is brand red", "cs('#overview','borderTopColor')", "rgb(228, 37, 27)"),
    ("header", "1px rule below", "cs('#overview','borderBottomColor')", "rgb(204, 204, 204)"),
    ("header", "no shadow", "cs('#overview','boxShadow')", "none"),
    ("header", "title is ink", "cs('#pageTitle','color')", "rgb(18, 18, 18)"),
    ("header", "subtitle is muted", "cs('#pageSubTitle','color')", "rgb(102, 102, 102)"),
    ("header", "logo file present and loaded", "String(document.querySelector('.logo.logoL').naturalWidth > 0)", "true"),
    ("header", "logo at least 60px wide", "String(parseFloat(cs('.logo.logoL','width')) >= 60)", "true"),
    ("frame", "navbar has no shadow", "cs('#topnav','boxShadow')", "none"),
    ("frame", "navbar is charcoal", "cs('#topnav .navbar-inner','backgroundColor')", "rgb(18, 18, 18)"),
    ("frame", "navbar above the header carries no rule (the header's red edge does)", "cs('#topnav .navbar-inner','borderBottomWidth')", "0px"),
    ("frame", "navbar below the header has a 4px rule", "cs('#pageLinks .navbar-inner','borderBottomWidth')", "4px"),
    ("frame", "navbar below-header rule is brand red", "cs('#pageLinks .navbar-inner','borderBottomColor')", "rgb(228, 37, 27)"),
    ("frame", "navbar links are white", "cs('#nav li:not(.activePage) a','color')", "rgb(255, 255, 255)"),
    ("frame", "current page sits on a lighter dark", "cs('#nav li.activePage a','backgroundColor')", "rgb(51, 51, 51)"),
    ("frame", "current page is underlined in brand red", "cs('#nav li.activePage a','boxShadow')", "rgb(228, 37, 27) 0px -3px 0px 0px inset"),
    ("frame", "sidebar is square", "cs('#toc','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar has no shadow", "cs('#toc','boxShadow')", "none"),
    ("frame", "sidebar has a 1px frame", "cs('#toc','borderTopWidth')", "1px"),
    ("frame", "sidebar frame is grey-30", "cs('#toc','borderTopColor')", "rgb(204, 204, 204)"),
    ("frame", "first sidebar item is square", "cs('#toc > li:first-child > a','borderTopLeftRadius')", "0px"),
    ("frame", "sidebar items have a 1px rule below", "cs('#toc > li:nth-child(2) > a','borderBottomWidth')", "1px"),
    ("frame", "sidebar item rule is grey-20", "cs('#toc > li:nth-child(2) > a','borderBottomColor')", "rgb(229, 229, 229)"),
    ("frame", "last sidebar item has no rule below the frame", "cs('#toc > li:last-child > a','borderBottomWidth')", "0px"),
    ("frame", "selected sidebar item has a 4px red left rule", "cs('#toc > li.active > a','borderLeftWidth')", "4px"),
    ("frame", "selected sidebar left rule is brand red", "cs('#toc > li.active > a','borderLeftColor')", "rgb(228, 37, 27)"),
    ("frame", "selected sidebar item sits on a pale red wash", "String(cs('#toc > li.active > a','backgroundColor') === v('color-mix(in srgb, var(--cu-red) 6%, var(--cu-bg))','backgroundColor'))", "true"),
    ("frame", "selected sidebar text is ink, not white on red", "cs('#toc > li.active > a','color')", "rgb(18, 18, 18)"),
    ("frame", "selected and unselected sidebar text line up", "(function(){var a=document.querySelector('#toc > li.active > a'),b=document.querySelector('#toc > li:nth-child(2) > a');return String(getComputedStyle(a).paddingLeft===getComputedStyle(b).paddingLeft&&getComputedStyle(a).borderLeftWidth===getComputedStyle(b).borderLeftWidth)})()", "true"),
    # The base template clears floats with `section { overflow: auto }` (custom.css), which also
    # clips a focus ring painted outside the section box - reported in test round 1.
    ("focus", "sections do not clip what is painted outside them", "cs('#test-section','overflow')", "visible"),
    ("focus", "sections still contain their floats", "cs('#test-section','display')", "flow-root"),
    ("focus", "float containment still works (section is as tall as its float)",
     "(function(){var s=document.querySelector('#test-section');return String(s.getBoundingClientRect().height>=60)})()", "true"),
    ("focus", "focus ring is 2px, offset 4px, ink",
     "(function(){var b=document.querySelector('#focus-btn'),previous=document.activeElement;b.focus({preventScroll:true});"
     "var s=getComputedStyle(b),result=(document.activeElement===b && b.matches(':focus-visible'))+' '+s.outlineStyle+' '+s.outlineWidth+' '+s.outlineOffset+' '+s.outlineColor;previous.focus({preventScroll:true});if(document.activeElement===b)b.blur();return result})()", "true solid 2px 4px rgb(18, 18, 18)"),
    # Test round 1: the toggle overflowed the bar and the header painted over the overflow.
    # Forcing it taller than the bar proves the bar now grows to contain it.
    ("frame", "navbar toggle stays inside the bar, even when taller than it",
     "(function(){var b=document.querySelector('#pageNavBtn');b.style.display='block';b.style.minHeight='64px';"
     "var r=b.getBoundingClientRect(),bar=document.querySelector('#topnav .navbar-inner').getBoundingClientRect();"
     "var ok=r.bottom<=bar.bottom+0.5&&r.top>=bar.top-0.5;b.style.display='';b.style.minHeight='';return String(ok)})()", "true"),
    # cardiffuni-v3.js publishes --cu-sticky-nav (the sticky page menu's height). These assert
    # the fallbacks that apply when it is absent or the bar is not sticky.
    ("focus", "sections carry a scroll margin for the sticky page menu", "cs('#test-section','scrollMarginTop')", "16px"),
    ("frame", "affixed section menu clears the top of the viewport", "cs('#toc-affixed','top')", "24px"),
    ("frame", "affixed section menu is not capped: the player makes a long one static instead",
     "cs('#toc-affixed','maxHeight') + ' ' + cs('#toc-affixed','overflowY')", "none visible"),
    # Xerte marks a page section's heading with .sectionTitle; it should read as the design
    # system's section heading (h2), not a lighter red variant of it.
    ("headings", "section title is ink, not red", "cs('#section-title','color')", "rgb(18, 18, 18)"),
    ("headings", "section title uses the display font", "cs('#section-title','fontFamily').split(',')[0].trim()", '"Franklin Gothic Heavy"'),
    ("headings", "section title weight matches a section heading", "cs('#section-title','fontWeight')", "800"),
    ("headings", "section title is the same size as a plain h2",
     "String(cs('#section-title','fontSize')===cs('#plain-h2','fontSize'))", "true"),
    ("headings", "section title keeps the heading's tight leading",
     "String(cs('#section-title','lineHeight')===cs('#plain-h2','lineHeight'))", "true"),
    ("header", "title is left aligned, not centred in the header", "cs('.titles','textAlign')", "left"),
    ("header", "title sits beside the logo, one gap away",
     "(function(){var logo=document.querySelector('.logo.logoL').getBoundingClientRect(),"
     "title=document.querySelector('#pageTitle').getBoundingClientRect(),"
     "gap=parseFloat(getComputedStyle(document.querySelector('#overview.logoL .container')).columnGap);"
     "return String(Math.abs(title.left-(logo.right+gap))<=2)})()", "true"),
    # cardiffuni-v3.js: the player makes #topnav sticky when the page menu sits above the header,
    # and the #pageLinks wrapper sticky when the author puts it below. Measuring only #topnav
    # left the second case at 0px, and with it the section menu's clearance and spy offset.
    ("stickynav", "theme script is loaded and exposes its hook", "String(typeof window.cardiffuniV3 === 'object')", "true"),
    ("stickynav", "no sticky page menu means no offset to clear",
     "(function(){window.cardiffuniV3.apply();"
     "return getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav').trim()})()", "0px"),
    ("stickynav", "a sticky bar above the header is measured",
     "(function(){var n=document.getElementById('topnav');n.style.position='sticky';n.style.top='0';"
     "window.cardiffuniV3.apply();"
     "var v=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav'));"
     "n.style.position='';n.style.top='';window.cardiffuniV3.apply();return String(v>0)})()", "true"),
    ("stickynav", "a sticky #pageLinks wrapper below the header is measured too",
     "(function(){var w=document.getElementById('pageLinks');w.style.position='sticky';w.style.top='0';"
     "window.cardiffuniV3.apply();"
     "var v=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav'));"
     "w.style.position='';w.style.top='';window.cardiffuniV3.apply();return String(v>0)})()", "true"),
    ("stickynav", "the section menu gets an inline top that beats the player's",
     "(function(){var w=document.getElementById('pageLinks'),m=document.querySelector('.bs-docs-sidenav');"
     "m.style.top='65px';w.style.position='sticky';w.style.top='0';window.cardiffuniV3.apply();"
     "var ok=m.style.top!=='65px'&&parseFloat(m.style.top)>0;"
     "w.style.position='';w.style.top='';window.cardiffuniV3.apply();m.style.top='';return String(ok)})()", "true"),
    # A section link lands with the heading scroll-margin-top below the top of the window. If the
    # spy switched exactly there, a sub-pixel rounding of the scroll position left the previous
    # item highlighted until the reader nudged the page (reported 21 September 2026).
    ("stickynav", "spy switches before a link's landing point, not exactly on it",
     "(function(){window.cardiffuniV3.apply();"
     "var margin=parseFloat(cs('#test-section','scrollMarginTop'));"
     "return String(window.__spy.options.offset - margin)})()", "8"),
    ("stickynav", "the spy offset follows the sticky bar too",
     "(function(){var w=document.getElementById('pageLinks');w.style.position='sticky';w.style.top='0';"
     "window.cardiffuniV3.apply();var withBar=window.__spy.options.offset;"
     "w.style.position='';w.style.top='';window.cardiffuniV3.apply();"
     "return String(withBar > window.__spy.options.offset)})()", "true"),
    # A host can enable smooth scrolling even though the theme no longer does.
    # Corrections must still land instantly and restore the host setting.
    ("stickynav", "the script corrects a landing instantly, not with a second animation",
     "(function(){var e=document.scrollingElement||document.documentElement;"
     "var before=e.style.scrollBehavior;e.style.scrollBehavior='smooth';"
     "document.body.style.minHeight='4000px';"
     "var sec=document.getElementById('test-section');"
     "location.hash='#test-section';window.cardiffuniV3.settleOnTarget();"
     "var landed=Math.round(window.pageYOffset);"
     "var wanted=Math.round(sec.getBoundingClientRect().top+window.pageYOffset-16);"
     "var restored=e.style.scrollBehavior==='smooth';e.style.scrollBehavior=before;"
     "location.hash='';document.body.style.minHeight='';window.scrollTo(0,0);"
     "return String(restored && Math.abs(landed-wanted)<=2)})()", "true"),
    # Raised by the Codex review, 21 September 2026.
    # The player renders each page asynchronously and announces it with contentLoaded, and moves
    # between pages with pushState, which fires no hashchange.
    ("stickynav", "the script follows the player's content lifecycle",
     "(async function(){await new Promise(r=>setTimeout(r,250));"
     "var n=document.getElementById('topnav');n.style.position='sticky';n.style.top='0';"
     "document.documentElement.style.setProperty('--cu-sticky-nav','0px');"
     "try{window.__playerHandlers.contentLoaded();await new Promise(r=>setTimeout(r,250));"
     "return String(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav'))===Math.round(n.getBoundingClientRect().height));}"
     "finally{n.style.position='';n.style.top='';window.cardiffuniV3.apply();}})()", "true"),
    # Opening the collapsed page menu makes the bar taller without resizing the window.
    ("stickynav", "a bar that changes height is re-measured",
     "(function(){var n=document.getElementById('topnav');n.style.position='sticky';n.style.top='0';"
     "var pad=document.createElement('div');pad.style.height='40px';"
     "n.querySelector('.navbar-inner').appendChild(pad);window.cardiffuniV3.apply();"
     "var grown=Math.round(n.getBoundingClientRect().height);"
     "var published=parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav'));"
     "pad.remove();n.style.position='';n.style.top='';window.cardiffuniV3.apply();"
     "return String(grown > 40 && Math.abs(published - grown) <= 1)})()", "true"),
    # Deliver the captured observer callback explicitly; virtual time does not guarantee rendering frames.
    ("stickynav", "resize observer watches both navbar candidates and schedules measurement",
     "(async function(){await new Promise(r=>setTimeout(r,250));"
     "var n=document.getElementById('topnav'),pad=document.createElement('div');"
     "n.style.position='sticky';n.style.top='0';await new Promise(r=>setTimeout(r,250));"
     "pad.style.height='40px';n.querySelector('.navbar-inner').appendChild(pad);"
     "try{var observer=window.__resizeObservers.find(o=>o.targets.includes(n) && o.targets.includes(document.getElementById('pageLinks')));"
     "if(!observer)return 'false';observer.deliver();await new Promise(r=>setTimeout(r,250));"
     "return String(Math.abs(parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--cu-sticky-nav'))-n.getBoundingClientRect().height)<=1);}"
     "finally{pad.remove();n.style.position='';n.style.top='';window.cardiffuniV3.apply();}})()", "true"),
    # Dragging the scrollbar produces no wheel, touch or key event, so it needs its own signal.
    ("stickynav", "dragging the scrollbar stops the script re-landing the page",
     "(function(){location.hash='#test-section';window.cardiffuniV3.startSettling();"
     "var before=window.cardiffuniV3.state().settling;"
     "window.dispatchEvent(new MouseEvent('mousedown'));"
     "var after=window.cardiffuniV3.state().settling;location.hash='';"
     "return String(before === true && after === false)})()", "true"),
    # Change the shared source and exercise old aliases and newer consumers together.
    ("theming", "brand role updates legacy utilities and the new header rule",
     "withRootTokens({'--cu-red':'rgb(0, 80, 140)'},()=>{const h=document.getElementById('overview'),old=h.style.transition;h.style.transition='none';try{return classStyle('bg-brand','backgroundColor')+' '+cs('#overview','borderTopColor');}finally{h.style.transition=old;}})",
     "rgb(0, 80, 140) rgb(0, 80, 140)"),
    ("theming", "spacing source updates legacy gap and section scroll margin",
     "withRootTokens({'--cu-space-4':'22px'},()=>classStyle('gap-md','gap')+' '+cs('#test-section','scrollMarginTop'))", "22px 22px"),
    ("theming", "body size follows the shared reading-copy role",
     "withRootTokens({'--cu-text-body':'21px'},()=>cs('body','fontSize'))", "21px"),
    ("theming", "all three heading sizes follow shared roles",
     "withRootTokens({'--cu-text-display':'50px','--cu-text-section':'35px','--cu-text-component':'27px'},()=>"
     "v('var(--h1-font-size)','fontSize')+' '+cs('#plain-h2','fontSize')+' '+v('var(--h3-font-size)','fontSize'))", "50px 35px 27px"),
    ("theming", "body font source reaches the theme alias without redeclaring it",
     "withRootTokens({'--cu-body':'monospace'},()=>cs('body','fontFamily'))", "monospace"),
    ("theming", "bold weight source reaches legacy utility",
     "withRootTokens({'--cu-weight-bold':'600'},()=>classStyle('font-bold','fontWeight'))", "600"),
    ("theming", "control rounding follows shared radius",
     "withRootTokens({'--cu-radius':'7px'},()=>classStyle('rounded','borderTopLeftRadius')+' '+v('var(--radius-card)','borderTopLeftRadius'))", "7px 0px"),
    ("theming", "overlay shadow follows shared shadow",
     "withRootTokens({'--cu-shadow-lg':'1px 2px 3px rgb(1, 2, 3)'},()=>v('var(--shadow-dropdown)','boxShadow'))", "rgb(1, 2, 3) 1px 2px 3px 0px"),
    ("theming", "fast transition follows shared duration and easing",
     "withRootTokens({'--cu-fast':'240ms','--cu-ease':'linear'},()=>v('var(--transition-fast)','transition'))", "0.24s linear"),
    ("theming", "light is derived from the shared white and surface roles, not a fixed value",
     "withRootTokens({'--cu-grey-10':'rgb(200, 200, 200)'},()=>{var c=rgbOf(v('var(--color-light)','backgroundColor'));return String(c[0]<235&&c[0]>220)})", "true"),
    ("theming", "legacy component overrides still work",
     "withRootTokens({'--font-size-body':'23px'},()=>cs('body','fontSize'))", "23px"),
    # Page chrome (21 September 2026). Colours follow the Red Usage Decisions log: the footer uses
    # no red, the feedback tab is action red, back-to-top and the glossary tip are ink.
    ("chrome", "footer sits on ink, not grey-80", "cs('#test-footer','backgroundColor')", "rgb(18, 18, 18)"),
    ("chrome", "footer secondary text is grey-30", "cs('#footer-note','color')", "rgb(204, 204, 204)"),
    ("chrome", "footer secondary text reads at 4.5:1 or better", "String(contrast('#footer-note','#test-footer')>=4.5)", "true"),
    # An h2 in the footer would otherwise take the section-heading size and the ink heading colour.
    ("chrome", "footer heading reads on the footer at 4.5:1 or better", "String(contrast('#footer-heading','#test-footer')>=4.5)", "true"),
    ("chrome", "footer heading is no bigger than a component heading",
     "String(parseFloat(cs('#footer-heading','fontSize'))<=parseFloat(v('var(--h3-font-size)','fontSize')))", "true"),
    ("chrome", "footer links read on the footer at 4.5:1 or better", "String(contrast('#footer-link','#test-footer')>=4.5)", "true"),
    # Measured by where the columns land: an auto-fit grid still lists its collapsed empty tracks.
    ("chrome", "author's footer columns sit side by side",
     "(function(){var k=document.querySelectorAll('#customFooter > div'),a=k[0].getBoundingClientRect(),b=k[1].getBoundingClientRect();"
     "return String(Math.abs(a.top-b.top)<=1 && b.left>=a.right)})()", "true"),
    ("chrome", "author's footer columns stack when the space is narrow",
     "(function(){var f=document.getElementById('customFooter');f.style.width='300px';"
     "var k=f.children,a=k[0].getBoundingClientRect(),b=k[1].getBoundingClientRect(),ok=b.top>=a.bottom-1&&Math.abs(a.left-b.left)<=1;"
     "f.style.width='';return String(ok)})()", "true"),
    ("chrome", "footer link list lines up with its heading (no bullet indent)",
     "(function(){var h=document.querySelector('#footer-heading').getBoundingClientRect(),"
     "a=document.querySelector('#footer-link').getBoundingClientRect();return String(Math.abs(a.left-h.left)<=1)})()", "true"),
    # A full-width WCAG link stopped auto-fit collapsing the empty tracks, squeezing two columns to a quarter each.
    ("chrome", "the two footer columns still share the width, WCAG link or not",
     "(function(){var f=document.getElementById('customFooter').getBoundingClientRect(),"
     "a=document.querySelector('#customFooter > div').getBoundingClientRect();return String(a.width>=f.width*0.4)})()", "true"),
    ("chrome", "the player's appended WCAG link takes its own row, not a third column",
     "(function(){var k=document.querySelectorAll('#customFooter > div'),col=k[1].getBoundingClientRect(),"
     "w=document.querySelector('#footer-wcag').getBoundingClientRect();"
     "return String(w.top>=col.bottom-1 && Math.abs(w.left-k[0].getBoundingClientRect().left)<=1)})()", "true"),
    ("chrome", "feedback tab is action red", "cs('#feedback_button','backgroundColor')", "rgb(194, 31, 22)"),
    ("chrome", "feedback tab has no shadow", "cs('#feedback_button','boxShadow')", "none"),
    ("chrome", "feedback tab text reads at 4.5:1 or better", "String(contrast('#feedback-link','#feedback_button')>=4.5)", "true"),
    ("chrome", "back-to-top is ink", "cs('#top-round','backgroundColor')", "rgb(18, 18, 18)"),
    ("chrome", "back-to-top has no resting shadow", "cs('#top-round','boxShadow')", "none"),
    ("chrome", "back-to-top has no hover halo", "ps('#top-round','::after','boxShadow')", "none"),
    ("chrome", "back-to-top arrow reads at 4.5:1 or better", "String(contrast('#top-round','#top-round')>=4.5)", "true"),
    # The player's .top-round sets `transition: all .3s !important`, so a reading taken the moment
    # the button is focused is the start of the ring's fade-in, not the ring itself.
    ("chrome", "back-to-top keeps a visible focus ring, offset from the ink",
     "(function(){var b=document.querySelector('#top-round'),previous=document.activeElement;"
     "b.style.setProperty('transition','none','important');b.focus({preventScroll:true});"
     "var s=getComputedStyle(b),result=(document.activeElement===b && b.matches(':focus-visible'))+' '+s.outlineStyle+' '+s.outlineWidth+' '+s.outlineOffset;"
     "b.style.removeProperty('transition');previous.focus({preventScroll:true});if(document.activeElement===b)b.blur();return result})()", "true solid 2px 4px"),
    # The global focus ring is ink, which disappears on an ink footer.
    ("chrome", "footer link focus ring is white, so it shows on the ink",
     "(function(){var a=document.querySelector('#footer-link'),previous=document.activeElement;a.focus({preventScroll:true});"
     "var s=getComputedStyle(a),result=(document.activeElement===a && a.matches(':focus-visible'))+' '+s.outlineStyle+' '+s.outlineWidth+' '+s.outlineColor;"
     "previous.focus({preventScroll:true});if(document.activeElement===a)a.blur();return result})()", "true solid 2px rgb(255, 255, 255)"),
    ("chrome", "glossary tip is ink", "cs('#glossaryHover','backgroundColor')", "rgb(18, 18, 18)"),
    ("chrome", "glossary tip reads at 4.5:1 or better", "String(contrast('#glossaryHover','#glossaryHover')>=4.5)", "true"),
    ("chrome", "glossary term is marked by more than colour",
     "String(parseFloat(cs('#glossary-term','borderBottomWidth'))>=1 && cs('#glossary-term','borderBottomStyle')!=='none')", "true"),
    # Alerts, badges and progress (21 September 2026). Danger and error states use the design
    # system's error red; the default progress fill is ink (Red Usage Decisions).
    ("status", "alert sits on the grey surface", "cs('#alert-info','backgroundColor')", "rgb(242, 242, 242)"),
    ("status", "alert corners are square", "cs('#alert-info','borderTopLeftRadius')", "0px"),
    ("status", "alert text is ink", "cs('#alert-info','color')", "rgb(18, 18, 18)"),
    ("status", "success alert rule is Forest Green", "cs('#alert-success','borderLeftColor')", "rgb(7, 135, 62)"),
    ("status", "info alert rule is link blue", "cs('#alert-info','borderLeftColor')", "rgb(4, 91, 198)"),
    ("status", "warning alert rule is Yellow", "cs('#alert-warning','borderLeftColor')", "rgb(255, 179, 0)"),
    ("status", "danger alert rule is the error red", "cs('#alert-danger','borderLeftColor')", "rgb(161, 26, 18)"),
    ("status", "error alert matches danger", "cs('#alert-error','borderLeftColor')", "rgb(161, 26, 18)"),
    # The glyph and the word carry the status, so the rule's colour is never the only cue.
    ("status", "warning alert keeps its glyph prefix", "ps('#alert-warning','::before','content')", '"⚠ "'),
    ("status", "every alert's text reads at 4.5:1 or better",
     "String(['success','info','warning','danger','error'].every(function(v){return contrast('#alert-'+v,'#alert-'+v)>=4.5}))", "true"),
    ("status", "a heading inside any alert is ink, not Bootstrap's per-variant colour",
     "String(['success','info','warning','danger','error'].map(function(v){return cs('#alert-h-'+v,'color')}).join('|'))",
     "|".join(["rgb(18, 18, 18)"] * 5)),
    ("status", "every badge and label reads at 4.5:1 or better",
     "String(['badge-default','badge-success','badge-warning','badge-important','badge-danger','badge-info','badge-inverse','label-default','label-info','label-danger']"
     ".every(function(i){return contrast('#'+i,'#'+i)>=4.5}))", "true"),
    ("status", "danger badge is the error red", "cs('#badge-danger','backgroundColor')", "rgb(161, 26, 18)"),
    ("status", "important badge is the error red", "cs('#badge-important','backgroundColor')", "rgb(161, 26, 18)"),
    ("status", "danger label is the error red", "cs('#label-danger','backgroundColor')", "rgb(161, 26, 18)"),
    ("status", "info badge is link blue", "cs('#badge-info','backgroundColor')", "rgb(4, 91, 198)"),
    ("status", "progress track has no shadow", "cs('#progress-track','boxShadow')", "none"),
    ("status", "progress track is square", "cs('#progress-track','borderTopLeftRadius')", "0px"),
    ("status", "default progress fill is ink", "cs('#bar-default','backgroundColor')", "rgb(18, 18, 18)"),
    ("status", "danger progress fill is the error red", "cs('#bar-danger','backgroundColor')", "rgb(161, 26, 18)"),
    ("status", "info progress fill is link blue", "cs('#bar-info','backgroundColor')", "rgb(4, 91, 198)"),
    ("status", "every progress fill shows against its track at 3:1 or better",
     "String(['default','success','warning','danger','info'].every(function(v){return contrast('#bar-'+v,'#progress-track','backgroundColor')>=3}))", "true"),
    ("status", "every progress label reads on its fill at 4.5:1 or better",
     "String(['default','success','warning','danger','info'].every(function(v){return contrast('#bar-'+v,'#bar-'+v)>=4.5}))", "true"),
    # Tables (21 September 2026). Wide tables only stay off the page when an author adds the
    # .cu-table-scroll wrapper: display:block would stop every table filling its container.
    ("tables", "table is square", "cs('#tbl','borderTopLeftRadius')", "0px"),
    ("tables", "table has no shadow, even if the shared shadow role changes",
     "withRootTokens({'--cu-shadow-sm':'1px 2px 3px rgb(1, 2, 3)'},()=>cs('#tbl','boxShadow'))", "none"),
    ("tables", "caption reads at 4.5:1 or better", "String(contrast('#tbl-caption','#tbl')>=4.5)", "true"),
    ("tables", "odd striped row is a quiet grey tint, not green", "cs('#td-odd','backgroundColor')", "rgb(242, 242, 242)"),
    ("tables", "even striped row has no fill", "cs('#td-even','backgroundColor')", "rgba(0, 0, 0, 0)"),
    ("tables", "striped text reads at 4.5:1 or better", "String(contrast('#td-odd','#td-odd')>=4.5)", "true"),
    ("tables", "a wrapped wide table does not stretch the page",
     "String(document.documentElement.scrollWidth<=document.documentElement.clientWidth)", "true"),
    ("tables", "the wrapper scrolls sideways", "cs('#tbl-scroll','overflowX')", "auto"),
    ("tables", "a wrapped narrow table still fills the wrapper",
     "String(Math.abs(document.getElementById('tbl-narrow').getBoundingClientRect().width-document.getElementById('tbl-scroll-narrow').clientWidth)<=1)", "true"),
    # Cards (21 September 2026): only the heading is smaller. --font-size-2xl is
    # clamp(1.5rem, 1.30rem + 1vw, 1.75rem), which is 28px at the fixture's 1280px width.
    ("cards", "card heading uses the 2xl size", "cs('#card-heading','fontSize')", "28px"),
    ("cards", "the clickable card's plain h3 matches", "cs('#card-heading-link','fontSize')", "28px"),
    ("cards", "card heading is smaller than a plain component heading",
     "String(parseFloat(cs('#card-heading','fontSize'))<parseFloat(cs('#plain-h3','fontSize')))", "true"),
    ("cards", "a component heading outside a card keeps its size", "cs('#plain-h3','fontSize')", "30px"),
    # --color-warning and --color-status-warning were the same token by two hops (both resolved
    # to the Draft label's black), so warning text and icons were indistinguishable from plain
    # ink (21 September 2026, addendum). --color-warning is renamed --color-draft: it is only
    # ever used for that one label.
    ("warning", "warning text matches the darkened warning orange, not ink",
     "String(sameColor(cs('#text-warning','color'),'rgb(163, 83, 21)'))", "true"),
    ("warning", "warning text reads at 4.5:1 or better on white", "String(contrast('#text-warning','body')>=4.5)", "true"),
    ("warning", "warning icon matches warning text, not ink",
     "String(sameColor(cs('#warning-icon','color'),cs('#text-warning','color')))", "true"),
    ("warning", "the draft label keeps its own black-on-yellow (10.4:1), unaffected by the rename",
     "cs('#draft-label','color')+' '+cs('#draft-label','backgroundColor')", "rgb(18, 18, 18) rgb(255, 179, 0)"),
    ("cards", "card description keeps the reading size", "cs('#card-desc','fontSize')", "18px"),
    ("tables", "the scroll wrapper shows the theme's focus ring when focused",
     "(function(){var b=document.querySelector('#tbl-scroll'),previous=document.activeElement;b.focus({preventScroll:true});"
     "var s=getComputedStyle(b),result=(document.activeElement===b && b.matches(':focus-visible'))+' '+s.outlineStyle+' '+s.outlineWidth+' '+s.outlineOffset+' '+s.outlineColor;"
     "previous.focus({preventScroll:true});if(document.activeElement===b)b.blur();return result})()", "true solid 2px 4px rgb(18, 18, 18)"),

]


def logo_checks():
    """Right-logo and two-logo headers (review Minor 10, and the two-logo case it did not mention)."""
    out = []
    for variant in VARIANTS:
        both = variant.startswith("both")
        first = ("#overview img.logoL" if both else "#overview .titles")
        def add(name, js, expected="true"):
            out.append(("logos", f"{variant}: {name}", js, expected, variant))
        add("content stays inside the window",
            "(function(){var w=document.documentElement.clientWidth;"
            "return String(['#overview .titles','#overview img.logoR','#overview img.logoL'].every(function(s){"
            "var e=document.querySelector(s);return !e||e.offsetParent===null||e.getBoundingClientRect().right<=w+0.5}))})()")
        add("title is left aligned", "cs('#overview .titles','textAlign')", "left")
        add("the right logo sits to the right of the title",
            "String(box('#overview .titles').right<=box('#overview img.logoR').left+1)")
        add("logo and title share a row",
            "(function(){var t=box('#overview .titles'),l=box('#overview img.logoR');return String(t.top<l.bottom&&l.top<t.bottom)})()")
        add("the right logo takes at most a quarter of the header",
            "String(box('#overview img.logoR').width<=document.querySelector('#overview .container').clientWidth*0.25+1)")
        # A maximum alone passes for a logo squeezed to a few pixels, so also require a minimum.
        add("the right logo is not squeezed below its own size or a quarter of the header",
            "(function(){var l=box('#overview img.logoR'),c=document.querySelector('#overview .container');"
            "return String(l.width>=Math.min(160,c.clientWidth*0.25)-1)})()")
        add("the right logo has the same side gutter as the first item",
            "(function(){var l=box('#overview img.logoR'),c=box('#overview .container'),f=box('%s');"
            "return String(Math.abs((c.right-l.right)-(f.left-c.left))<=2)})()" % first)
        add("the first item keeps a side gutter", f"String(box('{first}').left>=16)")
        if both:
            add("the Cardiff logo keeps its 70px minimum", "String(box('#overview img.logoL').width>=70)")
            add("left logo, title and right logo run in that order",
                "String(box('#overview img.logoL').right<=box('#overview .titles').left+1)")
    return out


CHECKS += logo_checks()


def run_chrome(page, width):
    run_file = HERE / ".fixture-run.html"
    run_file.write_text(page, encoding="utf-8")
    try:
        out = subprocess.run(
            [CHROME, "--headless=new", "--disable-gpu", "--allow-file-access-from-files",
             "--virtual-time-budget=5000", f"--window-size={width},900", "--dump-dom", run_file.as_uri()],
            capture_output=True, text=True, timeout=90,
        ).stdout
    finally:
        run_file.unlink(missing_ok=True)
    match = re.search(r'<pre id="results">(.*?)</pre>', out, re.S)
    if not match or not match.group(1).strip():
        sys.exit("ERROR: the fixture produced no results. Check the Chrome path and the fixture's script.")
    return json.loads(html.unescape(match.group(1)))


def evaluate(checks):
    by_variant = {}
    for check in checks:
        by_variant.setdefault(check[4] if len(check) > 4 else None, []).append(check)
    results = {}
    for variant, group in by_variant.items():
        width, header = VARIANTS[variant] if variant else (1280, None)
        page = FIXTURE.read_text(encoding="utf-8")
        if header is not None:
            page = re.sub(r'<header class="jumbotron logoL" id="overview">.*?</header>', lambda _: header, page, count=1, flags=re.S)
        exprs = {f"{c[0]}::{c[1]}": c[2] for c in group}
        results.update(run_chrome(page.replace("/*@CHECKS@*/", "const CHECKS = " + json.dumps(exprs) + ";"), width))
    return results


def main():
    groups = set(sys.argv[1:])
    selected = [c for c in CHECKS if not groups or c[0] in groups]
    if not selected:
        sys.exit(f"ERROR: no checks in groups {sorted(groups)}. Known: {sorted({c[0] for c in CHECKS})}")
    results = evaluate(selected)
    failed = 0
    for group, name, _, expected, *_variant in selected:
        actual = results.get(f"{group}::{name}", "NO RESULT")
        ok = actual == expected
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'}  [{group}] {name}" + ("" if ok else f"\n      expected {expected!r}, got {actual!r}"))
    print(f"\n{len(selected) - failed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
