/* ============================================================
   Inclusive Prehabilitation for People with Cancer
   Project-level JavaScript — loaded once via Xerte project
   settings (Scripts field).
   ============================================================ */

(function () {
  'use strict';

  /* ----------------------------------------------------------
     Audio Player (.ippc-audio-player)
     Builds interactive play/pause controls, a progress bar,
     and seek-on-click for every .ippc-audio-player element.

     Page markup (paste into Xerte HTML editor):

       <div class="ippc-audio-player">
         <span class="ippc-audio-title">EDIT: title</span>
         <span class="ippc-audio-size">EDIT: 0.0 MB</span>
         <audio class="ippc-audio" src="EDIT-path.mp3" preload="none" hidden></audio>
       </div>
  ---------------------------------------------------------- */

  function buildPlayer(card) {
    if (card.dataset.ippcBuilt) return;
    card.dataset.ippcBuilt = 'true';

    var titleEl = card.querySelector('.ippc-audio-title');
    var sizeEl  = card.querySelector('.ippc-audio-size');
    var audio   = card.querySelector('.ippc-audio');

    // Headphones icon
    var iconWrapper = document.createElement('div');
    iconWrapper.className = 'ippc-audio-icon';
    iconWrapper.innerHTML = '<i class="fas fa-headphones fa-2x" aria-hidden="true"></i>';
    card.insertBefore(iconWrapper, card.firstChild);

    // Info wrapper (title + size + progress bar)
    var infoWrapper = document.createElement('div');
    infoWrapper.className = 'ippc-audio-info';
    card.insertBefore(infoWrapper, titleEl);
    infoWrapper.appendChild(titleEl);
    if (sizeEl) infoWrapper.appendChild(sizeEl);

    // Progress bar
    var progress = document.createElement('div');
    progress.className = 'ippc-audio-progress';
    progress.setAttribute('role', 'progressbar');
    progress.setAttribute('aria-valuemin', '0');
    progress.setAttribute('aria-valuemax', '100');
    progress.setAttribute('aria-valuenow', '0');
    progress.setAttribute('aria-label', 'Audio progress');
    progress.innerHTML = '<div class="ippc-audio-progress__fill"></div>';
    infoWrapper.appendChild(progress);

    // Play/pause button
    var btn = document.createElement('button');
    btn.className = 'ippc-audio-btn';
    btn.setAttribute('aria-label', 'Play audio');
    btn.innerHTML = '<i class="fas fa-play" aria-hidden="true"></i>';
    card.insertBefore(btn, audio);
  }

  function setPlayState(btn, playing) {
    btn.querySelector('i').className = playing ? 'fas fa-pause' : 'fas fa-play';
    btn.setAttribute('aria-label', playing ? 'Pause audio' : 'Play audio');
  }

  function initAudioPlayers() {
    document.querySelectorAll('.ippc-audio-player').forEach(buildPlayer);
  }

  // Build any players already in the DOM
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAudioPlayers);
  } else {
    initAudioPlayers();
  }

  // Watch for players added dynamically by Xerte's page renderer
  var observer = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      mutation.addedNodes.forEach(function (node) {
        if (node.nodeType !== 1) return;
        if (node.classList && node.classList.contains('ippc-audio-player')) {
          buildPlayer(node);
        }
        if (node.querySelectorAll) {
          node.querySelectorAll('.ippc-audio-player').forEach(buildPlayer);
        }
      });
    });
  });

  observer.observe(document.body || document.documentElement, {
    childList: true,
    subtree: true
  });

  /* ----------------------------------------------------------
     Slider (.ippc-slider)
     Builds prev/next arrows and dot navigation for every
     .ippc-slider element. Add .ippc-slider-slide <div>s as
     direct children of .ippc-slider in the page HTML.
  ---------------------------------------------------------- */

  function buildSlider(container) {
    if (container.dataset.ippcBuilt) return;
    container.dataset.ippcBuilt = 'true';

    var slides = Array.from(container.querySelectorAll('.ippc-slider-slide'));
    var total  = slides.length;
    var current = 0;

    if (total === 0) return;

    var track = document.createElement('div');
    track.className = 'ippc-slider-track';
    slides.forEach(function (slide) { track.appendChild(slide); });
    container.appendChild(track);

    var nav = document.createElement('div');
    nav.className = 'ippc-slider-nav';

    var prevBtn = document.createElement('button');
    prevBtn.className = 'ippc-slider-arrow';
    prevBtn.setAttribute('aria-label', 'Previous slide');
    prevBtn.innerHTML = '<i class="fas fa-chevron-left" aria-hidden="true"></i>';

    var dotsWrapper = document.createElement('div');
    dotsWrapper.className = 'ippc-slider-dots';
    dotsWrapper.setAttribute('role', 'tablist');
    dotsWrapper.setAttribute('aria-label', 'Slides');

    var dots = slides.map(function (_, i) {
      var dot = document.createElement('button');
      dot.className = 'ippc-slider-dot';
      dot.setAttribute('role', 'tab');
      dot.setAttribute('aria-label', 'Slide ' + (i + 1) + ' of ' + total);
      dot.addEventListener('click', function () { goTo(i); });
      dotsWrapper.appendChild(dot);
      return dot;
    });

    var nextBtn = document.createElement('button');
    nextBtn.className = 'ippc-slider-arrow';
    nextBtn.setAttribute('aria-label', 'Next slide');
    nextBtn.innerHTML = '<i class="fas fa-chevron-right" aria-hidden="true"></i>';

    nav.appendChild(prevBtn);
    nav.appendChild(dotsWrapper);
    nav.appendChild(nextBtn);
    container.appendChild(nav);

    function goTo(index) {
      if (index < 0 || index >= total) return;
      slides[current].classList.remove('active');
      dots[current].classList.remove('active');
      dots[current].setAttribute('aria-selected', 'false');
      current = index;
      slides[current].classList.add('active');
      dots[current].classList.add('active');
      dots[current].setAttribute('aria-selected', 'true');
      prevBtn.disabled = current === 0;
      nextBtn.disabled = current === total - 1;
    }

    container.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft')  goTo(current - 1);
      if (e.key === 'ArrowRight') goTo(current + 1);
    });

    prevBtn.addEventListener('click', function () { goTo(current - 1); });
    nextBtn.addEventListener('click', function () { goTo(current + 1); });

    goTo(0);
  }

  function initSliders() {
    document.querySelectorAll('.ippc-slider').forEach(buildSlider);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initSliders);
  } else {
    initSliders();
  }

  // Watch for sliders added dynamically by Xerte's page renderer
  var sliderObserver = new MutationObserver(function (mutations) {
    mutations.forEach(function (mutation) {
      mutation.addedNodes.forEach(function (node) {
        if (node.nodeType !== 1) return;
        if (node.classList && node.classList.contains('ippc-slider')) {
          buildSlider(node);
        }
        if (node.querySelectorAll) {
          node.querySelectorAll('.ippc-slider').forEach(buildSlider);
        }
      });
    });
  });

  sliderObserver.observe(document.body || document.documentElement, {
    childList: true,
    subtree: true
  });

  // Global event listeners — registered once
  // Play / pause button + seek on progress bar click
  document.addEventListener('click', function (e) {
    // Seek: click anywhere on the progress track
    var progress = e.target.closest('.ippc-audio-progress');
    if (progress) {
      var card  = progress.closest('.ippc-audio-player');
      var audio = card.querySelector('.ippc-audio');
      if (audio && audio.duration) {
        var rect  = progress.getBoundingClientRect();
        var ratio = Math.min(Math.max((e.clientX - rect.left) / rect.width, 0), 1);
        audio.currentTime = ratio * audio.duration;
      }
      return;
    }

    // Play / pause button
    var btn = e.target.closest('.ippc-audio-btn');
    if (!btn) return;

    var card  = btn.closest('.ippc-audio-player');
    var audio = card.querySelector('.ippc-audio');
    if (!audio) return;

    if (audio.paused) {
      // Pause any other playing audio first
      document.querySelectorAll('.ippc-audio').forEach(function (a) {
        if (a !== audio && !a.paused) {
          a.pause();
          setPlayState(a.closest('.ippc-audio-player').querySelector('.ippc-audio-btn'), false);
        }
      });
      audio.play();
      setPlayState(btn, true);
    } else {
      audio.pause();
      setPlayState(btn, false);
    }
  });

  // Advance progress bar (timeupdate doesn't bubble — capture phase)
  document.addEventListener('timeupdate', function (e) {
    if (!e.target.classList.contains('ippc-audio')) return;
    var card = e.target.closest('.ippc-audio-player');
    if (!card || !e.target.duration) return;
    var pct  = (e.target.currentTime / e.target.duration) * 100;
    var fill = card.querySelector('.ippc-audio-progress__fill');
    var bar  = card.querySelector('.ippc-audio-progress');
    if (fill) fill.style.width = pct + '%';
    if (bar)  bar.setAttribute('aria-valuenow', Math.round(pct));
  }, true);

  // Reset button + bar when audio finishes (ended doesn't bubble — capture phase)
  document.addEventListener('ended', function (e) {
    if (!e.target.classList.contains('ippc-audio')) return;
    var card = e.target.closest('.ippc-audio-player');
    if (!card) return;
    setPlayState(card.querySelector('.ippc-audio-btn'), false);
    var fill = card.querySelector('.ippc-audio-progress__fill');
    var bar  = card.querySelector('.ippc-audio-progress');
    if (fill) fill.style.width = '0%';
    if (bar)  bar.setAttribute('aria-valuenow', '0');
  }, true);

}());
