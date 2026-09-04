/* ============================================================================
   Figure interaction runtime
   ----------------------------------------------------------------------------
   Progressive enhancement only. Without this script every diagram still renders
   complete and readable; the script adds controls on top.

   Declared entirely with data attributes inside each <svg>. See INTERACTIVE.md.

     <svg data-steps='["First label","Second label"]'>   step through the build
       <g data-step="2">            appears when step 2 is reached, then stays
       <g data-step="2" data-only>  visible only while step 2 is current
       <g data-pulse>               draws attention when its step arrives

     <svg data-layers='[{"k":"a","label":"Option A"},{"k":"b","label":"Option B"}]'>
       <g data-layer="a">           shown only while layer a is selected

       <g data-hot="Short title" data-tip="The sentence this part is worth.">
                                    hoverable, tappable, focusable hotspot

   Everything is scoped per figure, so several diagrams can share a page and the
   same diagram can appear twice.
   ========================================================================== */
(function () {
  "use strict";

  var REDUCED = window.matchMedia &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var uid = 0;

  function parse(el, attr, fallback) {
    var raw = el.getAttribute(attr);
    if (!raw) return fallback;
    try { return JSON.parse(raw); } catch (e) { return fallback; }
  }

  function make(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function enhance(fig) {
    if (fig.dataset.fx === "1") return;
    var svg = fig.querySelector("svg");
    if (!svg) return;
    fig.dataset.fx = "1";
    uid++;

    var steps = parse(svg, "data-steps", null);
    var layers = parse(svg, "data-layers", null);
    var hots = Array.prototype.slice.call(svg.querySelectorAll("[data-hot]"));
    if (!steps && !layers && !hots.length) return;

    /* The drawing is about to gain controls and focusable parts, so it is no longer a
       single image. Keep the label, drop role="img" so the parts inside are reachable. */
    if (hots.length && svg.getAttribute("role") === "img") {
      svg.setAttribute("role", "group");
    }

    var bar = make("div", "fig-controls");
    var baseline = null;   /* what the readout says when no hotspot is active */
    var readout = make("div", "fig-readout");
    readout.setAttribute("aria-live", "polite");

    /* ---------------- hotspots ---------------- */
    var pinned = null;
    function showTip(el) {
      var title = el.getAttribute("data-hot") || "";
      var body = el.getAttribute("data-tip") || "";
      readout.innerHTML = "";
      readout.appendChild(make("b", null, title));
      if (body) readout.appendChild(make("span", null, " " + body));
      readout.classList.add("on");
      hots.forEach(function (h) { h.classList.toggle("is-active", h === el); });
    }
    function clearTip() {
      if (pinned) return;
      hots.forEach(function (h) { h.classList.remove("is-active"); });
      if (baseline) {
        readout.innerHTML = "";
        readout.appendChild(make("b", null, baseline.title));
        readout.appendChild(make("span", null, " " + baseline.body));
        readout.classList.add("on");
      } else {
        readout.classList.remove("on");
        readout.textContent = hots.length ? hotHint : "";
      }
    }

    function setBaseline(title, body) {
      baseline = { title: title, body: body };
      if (!pinned) clearTip();
    }
    var hotHint = hots.length
      ? (matchMedia("(hover: none)").matches
          ? "Tap any highlighted part of the diagram."
          : "Hover or tab through the highlighted parts of the diagram.")
      : "";

    hots.forEach(function (el) {
      el.classList.add("fig-hot");
      el.setAttribute("tabindex", "0");
      el.setAttribute("role", "button");
      var t = el.getAttribute("data-hot") || "";
      var b = el.getAttribute("data-tip") || "";
      el.setAttribute("aria-label", b ? t + ". " + b : t);
      el.addEventListener("mouseenter", function () { showTip(el); });
      el.addEventListener("mouseleave", clearTip);
      el.addEventListener("focus", function () { showTip(el); });
      el.addEventListener("blur", clearTip);
      el.addEventListener("click", function (e) {
        e.stopPropagation();
        pinned = (pinned === el) ? null : el;
        pinned ? showTip(el) : clearTip();
      });
      el.addEventListener("keydown", function (e) {
        if (e.key === "Enter" || e.key === " ") { e.preventDefault(); el.click(); }
      });
    });
    if (hots.length) {
      fig.addEventListener("click", function (e) {
        if (e.target.closest && e.target.closest(".fig-controls")) return;
        pinned = null; clearTip();
      });
      readout.textContent = hotHint;
    }

    /* ---------------- layers ---------------- */
    var layerEls = {};
    if (layers && layers.length) {
      layers.forEach(function (L) {
        layerEls[L.k] = Array.prototype.slice.call(
          svg.querySelectorAll('[data-layer="' + L.k + '"]'));
      });
      var group = make("div", "fig-seg");
      group.setAttribute("role", "group");
      group.setAttribute("aria-label", "Choose what the diagram shows");
      layers.forEach(function (L, i) {
        var b = make("button", "fig-segbtn", L.label);
        b.type = "button";
        b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
        b.addEventListener("click", function () {
          Array.prototype.forEach.call(group.children, function (c) {
            c.setAttribute("aria-pressed", c === b ? "true" : "false");
          });
          setLayer(L.k);
          if (L.note) setBaseline(L.label, L.note);
        });
        group.appendChild(b);
      });
      bar.appendChild(group);
      function setLayer(k) {
        Object.keys(layerEls).forEach(function (key) {
          layerEls[key].forEach(function (el) { el.classList.toggle("fig-off", key !== k); });
        });
      }
      setLayer(layers[0].k);
      if (layers[0].note) setBaseline(layers[0].label, layers[0].note);
    }

    /* ---------------- steps ---------------- */
    if (steps && steps.length) {
      var stepEls = Array.prototype.slice.call(svg.querySelectorAll("[data-step]"));
      var at = 1, n = steps.length;

      var prev = make("button", "fig-btn", "‹");
      prev.type = "button"; prev.setAttribute("aria-label", "Previous step");
      var next = make("button", "fig-btn fig-btn-primary", "Next ›");
      next.type = "button";
      var all = make("button", "fig-btn fig-btn-ghost", "Show all");
      all.type = "button";
      var dots = make("div", "fig-dots");
      var count = make("span", "fig-count");

      for (var i = 1; i <= n; i++) {
        (function (k) {
          var d = make("button", "fig-dot");
          d.type = "button";
          d.setAttribute("aria-label", "Step " + k + ": " + steps[k - 1]);
          d.addEventListener("click", function () { go(k); });
          dots.appendChild(d);
        })(i);
      }

      prev.addEventListener("click", function () { go(at - 1); });
      next.addEventListener("click", function () { go(at >= n ? 1 : at + 1); });
      all.addEventListener("click", function () { go(n + 1); });

      bar.appendChild(prev); bar.appendChild(next); bar.appendChild(dots);
      bar.appendChild(count); bar.appendChild(all);

      function go(k) {
        at = Math.max(1, Math.min(n + 1, k));
        var showAll = at > n;
        stepEls.forEach(function (el) {
          var s = parseInt(el.getAttribute("data-step"), 10) || 1;
          var only = el.hasAttribute("data-only");
          var on = showAll ? (!only || s === n) : (only ? s === at : s <= at);
          el.classList.toggle("fig-off", !on);
          var arriving = !REDUCED && !showAll && on && s === at;
          el.classList.toggle("fig-now", arriving);
          el.classList.toggle("fig-pulse", arriving && el.hasAttribute("data-pulse"));
        });
        Array.prototype.forEach.call(dots.children, function (d, i) {
          d.classList.toggle("on", !showAll && i + 1 === at);
          d.classList.toggle("done", showAll || i + 1 < at);
        });
        count.textContent = showAll ? "all steps" : at + " of " + n;
        prev.disabled = at === 1;
        next.textContent = at >= n ? "Replay" : "Next ›";
        all.setAttribute("aria-pressed", showAll ? "true" : "false");
        setBaseline(showAll ? "The whole picture." : "Step " + at + ".",
                    showAll ? (hotHint || "Every part of the diagram is now showing.")
                            : steps[at - 1]);
      }
      go(1);
    }

    /* ---------------- mount ---------------- */
    var cap = fig.querySelector("figcaption");
    if (bar.childNodes.length) fig.insertBefore(bar, cap || null);
    if (steps || layers || hots.length) fig.insertBefore(readout, cap || null);
    fig.classList.add("fig-interactive");
  }

  function scan(root) {
    (root || document).querySelectorAll("figure.ch-fig").forEach(enhance);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () { scan(); });
  } else { scan(); }

  /* the book reader clones a figure into its lightbox; re enhance the copy */
  window.enhanceFigures = scan;
})();
