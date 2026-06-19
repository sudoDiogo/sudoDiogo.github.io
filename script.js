// ============================================
// MATRIX / BINARY RAIN BACKGROUND
// ============================================
(function initMatrixRain() {
  const canvas = document.getElementById('matrix-bg');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');

  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let columns = [];
  let fontSize = 16;
  let frame = 0;

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    const columnCount = Math.floor(canvas.width / fontSize);
    columns = new Array(columnCount).fill(0).map(() => Math.floor(Math.random() * -50));
  }

  function draw() {
    ctx.fillStyle = 'rgba(7, 11, 18, 0.07)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.font = fontSize + 'px JetBrains Mono, monospace';

    for (let i = 0; i < columns.length; i++) {
      const char = Math.random() > 0.5 ? '1' : '0';
      const x = i * fontSize;
      const y = columns[i] * fontSize;

      const isHead = Math.random() > 0.975;
      ctx.fillStyle = isHead ? '#00d4ff' : '#00ff9d';

      ctx.fillText(char, x, y);

      if (y > canvas.height && Math.random() > 0.975) {
        columns[i] = 0;
      } else {
        columns[i]++;
      }
    }
  }

  function loop() {
    frame++;
    // throttle slightly for a calmer rain
    if (frame % 2 === 0) draw();
    requestAnimationFrame(loop);
  }

  window.addEventListener('resize', resize);
  resize();

  if (!prefersReducedMotion) {
    requestAnimationFrame(loop);
  } else {
    // static single frame for reduced motion users
    draw();
  }
})();

// ============================================
// MOBILE NAV TOGGLE
// ============================================
(function initNavToggle() {
  const toggle = document.getElementById('navToggle');
  const links = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const isOpen = links.classList.toggle('open');
    toggle.classList.toggle('open', isOpen);
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  links.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => {
      links.classList.remove('open');
      toggle.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
})();

// ============================================
// ACTIVE NAV LINK ON SCROLL
// ============================================
(function initActiveNav() {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  if (!sections.length || !navLinks.length) return;

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const id = entry.target.getAttribute('id');
          navLinks.forEach((link) => {
            link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
          });
        }
      });
    },
    { rootMargin: '-45% 0px -45% 0px', threshold: 0 }
  );

  sections.forEach((section) => observer.observe(section));
})();

// ============================================
// SCROLL REVEAL
// ============================================
(function initScrollReveal() {
  const targets = document.querySelectorAll(
    '.project-card, .contact-card, .section-head, .contact-inner'
  );
  targets.forEach((el) => el.classList.add('reveal'));

  const revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          revealObserver.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  targets.forEach((el) => revealObserver.observe(el));
})();

// ============================================
// FOOTER YEAR
// ============================================
(function setFooterYear() {
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();
