/**
 * Adds a collapsed "Show HTML" snippet with a Copy button under every demo example.
 *
 * The snippet is the example's own markup, read from the page, so it can never disagree with what is
 * shown. It leaves out the demo's own scaffolding, which an author must not paste into Xerte:
 *   - the block title, description and class label, and any sub-heading label (.demo-block-title)
 *   - wrappers that only carry demo-* classes (.demo-inline, .demo-container) are unwrapped
 *   - demo-* classes on other elements (.demo-box) are removed
 * A block is left alone when it has its own <pre>, or it or a section around it has data-code="skip"
 * (the Usage Guidelines sections).
 */
(function () {
    'use strict';

    var CHROME = /(^|\s)(demo-block__title|demo-block__description|code-label|demo-block-title|demo-code)(\s|$)/;
    var VOID = /^(area|base|br|col|embed|hr|img|input|link|meta|source|track|wbr)$/;
    var INLINE = /^(a|abbr|b|button|cite|code|em|i|img|input|kbd|label|mark|small|span|strong|sub|sup|u|br|select|textarea)$/;

    function escapeText(text) {
        return text.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }

    function escapeAttribute(value) {
        return value.replace(/&/g, '&amp;').replace(/"/g, '&quot;');
    }

    function isDemoOnly(el) {
        var classes = Array.prototype.slice.call(el.classList);
        return classes.length > 0 && classes.every(function (c) { return c.indexOf('demo-') === 0; });
    }

    // Copy of a node without the demo's scaffolding. Returns an array, because an unwrapped wrapper becomes its children.
    function clean(node) {
        if (node.nodeType !== 1) {
            return [node.cloneNode(false)];
        }
        var children = [];
        Array.prototype.forEach.call(node.childNodes, function (child) {
            if (child.nodeType === 1 && CHROME.test(child.className)) {
                return;
            }
            children = children.concat(clean(child));
        });
        var wrapperOnly = isDemoOnly(node) && node.attributes.length === 1 && !VOID.test(node.localName);
        if (wrapperOnly) {
            return children;
        }
        var copy = node.cloneNode(false);
        Array.prototype.slice.call(copy.classList).forEach(function (c) {
            if (c.indexOf('demo-') === 0) { copy.classList.remove(c); }
        });
        if (node.hasAttribute('class') && !copy.classList.length) {
            copy.removeAttribute('class');
        }
        children.forEach(function (child) { copy.appendChild(child); });
        return [copy];
    }

    function openTag(el) {
        var attrs = Array.prototype.map.call(el.attributes, function (a) {
            return a.value === '' ? ' ' + a.name : ' ' + a.name + '="' + escapeAttribute(a.value) + '"';
        }).join('');
        return '<' + el.localName + attrs + '>';
    }

    function inlineOnly(el) {
        return Array.prototype.every.call(el.childNodes, function (c) {
            return c.nodeType === 3 || c.nodeType === 8 || (c.nodeType === 1 && INLINE.test(c.localName) && inlineOnly(c));
        });
    }

    function flat(el) {
        if (VOID.test(el.localName)) { return openTag(el); }
        var inner = Array.prototype.map.call(el.childNodes, function (c) {
            if (c.nodeType === 3) { return escapeText(c.nodeValue).replace(/\s+/g, ' '); }
            if (c.nodeType === 8) { return '<!--' + c.nodeValue + '-->'; }
            return flat(c);
        }).join('');
        return openTag(el) + inner.trim() + '</' + el.localName + '>';
    }

    // Lines for one node at one indent level.
    function lines(node, depth) {
        var pad = new Array(depth + 1).join('  ');
        if (node.nodeType === 3) {
            var text = node.nodeValue.replace(/\s+/g, ' ').trim();
            return text ? [pad + escapeText(text)] : [];
        }
        if (node.nodeType === 8) { return [pad + '<!--' + node.nodeValue + '-->']; }
        if (VOID.test(node.localName) || inlineOnly(node)) { return [pad + flat(node)]; }
        var out = [pad + openTag(node)];
        Array.prototype.forEach.call(node.childNodes, function (c) { out = out.concat(lines(c, depth + 1)); });
        out.push(pad + '</' + node.localName + '>');
        return out;
    }

    function snippet(block) {
        var out = [];
        Array.prototype.forEach.call(block.children, function (child) {
            if (CHROME.test(child.className)) { return; }
            clean(child).forEach(function (node) { out = out.concat(lines(node, 0)); });
        });
        return out.join('\n');
    }

    function copy(text, done) {
        function fallback() {
            var area = document.createElement('textarea');
            area.value = text;
            area.setAttribute('readonly', '');
            area.style.position = 'fixed';
            area.style.opacity = '0';
            document.body.appendChild(area);
            area.select();
            var ok = false;
            try { ok = document.execCommand('copy'); } catch (e) { ok = false; }
            document.body.removeChild(area);
            done(ok);
        }
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(function () { done(true); }, fallback);
        } else {
            fallback();
        }
    }

    function build(block, text) {
        var details = document.createElement('details');
        details.className = 'demo-code';
        var summary = document.createElement('summary');
        summary.textContent = 'Show HTML';
        var body = document.createElement('div');
        body.className = 'demo-code__body';
        var button = document.createElement('button');
        button.type = 'button';
        button.className = 'demo-code__copy';
        button.textContent = 'Copy';
        var status = document.createElement('span');
        status.className = 'demo-code__status';
        status.setAttribute('role', 'status');
        var pre = document.createElement('pre');
        var code = document.createElement('code');
        code.textContent = text;
        pre.appendChild(code);
        body.appendChild(button);
        body.appendChild(status);
        body.appendChild(pre);
        details.appendChild(summary);
        details.appendChild(body);
        button.addEventListener('click', function () {
            copy(text, function (ok) {
                status.textContent = ok ? 'Copied' : 'Copy failed. Select the code and copy it.';
                setTimeout(function () { status.textContent = ''; }, 2500);
            });
        });
        block.appendChild(details);
    }

    function init() {
        Array.prototype.forEach.call(document.querySelectorAll('.demo-block'), function (block) {
            if (block.querySelector('pre') || block.closest('[data-code="skip"]')) { return; }
            var text = snippet(block);
            if (text) { build(block, text); }
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
}());
