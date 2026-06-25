/* ==============================================
   MATRIX / BINARY RAIN
   ============================================== */
(function () {
  const canvas = document.getElementById('matrix-bg');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let cols = [], frame = 0;
  const FS = 16;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    const n = Math.floor(canvas.width / FS);
    cols = Array.from({ length: n }, () => Math.floor(Math.random() * -60));
  }

  function draw() {
    ctx.fillStyle = 'rgba(7,11,18,0.07)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = FS + 'px JetBrains Mono, monospace';
    cols.forEach((y, i) => {
      ctx.fillStyle = Math.random() > 0.975 ? '#00d4ff' : '#00ff9d';
      ctx.fillText(Math.random() > 0.5 ? '1' : '0', i * FS, y * FS);
      if (y * FS > canvas.height && Math.random() > 0.975) cols[i] = 0;
      else cols[i]++;
    });
  }

  function loop() { if (frame++ % 2 === 0) draw(); requestAnimationFrame(loop); }

  window.addEventListener('resize', resize);
  resize();
  if (!reduced) requestAnimationFrame(loop); else draw();
})();

/* ==============================================
   NAV TOGGLE (mobile)
   ============================================== */
(function () {
  const toggle = document.getElementById('navToggle');
  const links  = document.querySelector('.nav-links');
  if (!toggle || !links) return;

  toggle.addEventListener('click', () => {
    const open = links.classList.toggle('open');
    toggle.classList.toggle('open', open);
    toggle.setAttribute('aria-expanded', String(open));
  });
  links.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
    links.classList.remove('open');
    toggle.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }));
})();

/* ==============================================
   ACTIVE NAV ON SCROLL
   ============================================== */
(function () {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks  = document.querySelectorAll('.nav-link');
  if (!sections.length) return;

  new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        const id = e.target.id;
        navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + id));
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' }).observe(
    // observe all sections
    ...[...sections].map(s => (new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting)
          navLinks.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id));
      });
    }, { rootMargin: '-45% 0px -45% 0px' }).observe(s), s))
  );
})();

/* ==============================================
   FOOTER YEAR
   ============================================== */
(function () {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();

/* ==============================================
   SCROLL REVEAL (applied after cards render too)
   ============================================== */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('is-visible'); revealObs.unobserve(e.target); }
  });
}, { threshold: 0.08 });

function enableReveal(root) {
  root.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));
}

document.querySelectorAll('.section-head, .stack-card').forEach(el => {
  el.classList.add('reveal');
  revealObs.observe(el);
});

/* ==============================================
   PROJECT CARD RENDERER
   ============================================== */
(function () {
  const grid = document.getElementById('projects-grid');
  if (!grid || typeof PROJECTS === 'undefined') return;

  // small inline SVGs
  const ICON_PROJECT = `<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M9 18V5l12-2v13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    <circle cx="6" cy="18" r="3" stroke="currentColor" stroke-width="1.5"/>
    <circle cx="18" cy="16" r="3" stroke="currentColor" stroke-width="1.5"/>
  </svg>`;

  function chipIcon(type) {
    if (type === 'pdf') return `<svg viewBox="0 0 16 16" fill="none" width="13" height="13">
      <path d="M3 1h7l3 3v11H3V1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M10 1v3h3M5 8h6M5 11h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`;
    if (type === 'py') return `<svg viewBox="0 0 16 16" fill="none" width="13" height="13">
      <path d="M3 1h7l3 3v11H3V1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M10 1v3h3M5 7l2.5 2L5 11M9 11h2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>`;
    return `<svg viewBox="0 0 16 16" fill="none" width="13" height="13">
      <path d="M3 1h7l3 3v11H3V1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M10 1v3h3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`;
  }

  function fileType(path) {
    const ext = (path || '').split('.').pop().toLowerCase();
    return ext === 'pdf' ? 'pdf' : ext === 'py' ? 'py' : ext === 'png' || ext === 'jpg' || ext === 'jpeg' ? 'img' : 'other';
  }

  grid.innerHTML = '';

  PROJECTS.forEach((proj, pidx) => {
    const hasFiles = proj.files && proj.files.length > 0;
    const done = proj.status === 'concluído';

    const card = document.createElement('article');
    card.className = 'project-card reveal';
    card.dataset.pidx = pidx;

    // build file chips html
    let filesHTML = '';
    if (hasFiles) {
      const chips = proj.files.map((f, fidx) => {
        const t = fileType(f.path);
        return `<button class="file-chip" data-pidx="${pidx}" data-fidx="${fidx}" type="button">
          ${chipIcon(t)}<span>${f.label}</span>
        </button>`;
      }).join('');
      filesHTML = `<div class="card-files"><p class="card-files-label">arquivos</p><div class="card-chip-row">${chips}</div></div>`;
    }

    // concepts
    const tagsHTML = (proj.concepts || []).map(c => `<span class="concept-tag">${c}</span>`).join('');

    card.innerHTML = `
      <div class="card-top">
        <span class="file-tag">${proj.tag}</span>
        <span class="status-pill ${done ? 'status-pill--done' : ''}">${proj.status}</span>
      </div>
      <div class="card-body-row">
        <div class="card-left">
          <div class="card-icon">${ICON_PROJECT}</div>
          <h3 class="card-title">${proj.title}</h3>
          <p class="card-text">${proj.desc}</p>
          ${filesHTML}
        </div>
        <div class="card-right">
          <p class="card-aside-label">tecnologias</p>
          <div class="card-tech-row">
            ${(proj.tech || []).map(t => `<span class="tech-badge">${t}</span>`).join('')}
          </div>
          <p class="card-aside-label" style="margin-top:1rem">técnicas</p>
          <div class="card-concepts-row">${tagsHTML}</div>
        </div>
      </div>
    `;

    grid.appendChild(card);
  });

  // store globally so modal can access
  window._PROJECTS = PROJECTS;

  // kick off reveal for newly created cards
  enableReveal(grid);
})();

/* ==============================================
   MODAL — visualizador de arquivos
   ============================================== */
(function () {
  const overlay  = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalClose');
  const bodyEl   = document.getElementById('modalBody');
  const titleEl  = document.getElementById('modalTitle');
  const badgeEl  = document.getElementById('modalBadge');
  const tabsEl   = document.getElementById('modalFileTabs');

  if (!overlay || !closeBtn) return;

  let _proj  = null;
  let _fidx  = 0;

  /* ---------- open / close ---------- */
  function openModal(pidx, fidx) {
    const projects = window._PROJECTS;
    if (!projects || !projects[pidx]) return;
    _proj = projects[pidx];
    _fidx = fidx;
    render();
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden'; // lock scroll on <html>
    closeBtn.focus();
  }

  function closeModal() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = ''; // restore scroll
    // wipe content so iframe stops loading
    setTimeout(() => { bodyEl.innerHTML = ''; tabsEl.innerHTML = ''; }, 300);
  }

  /* ---------- file type ---------- */
  function ftype(path) {
    const ext = (path || '').split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (ext === 'py')  return 'py';
    if (['png','jpg','jpeg','gif','webp'].includes(ext)) return 'img';
    return 'other';
  }

  /* ---------- render ---------- */
  function render() {
    const file = _proj.files[_fidx];
    if (!file) return;
    const type = ftype(file.path);

    // badge
    badgeEl.textContent = type.toUpperCase();
    badgeEl.className   = 'modal-badge modal-badge--' + type;
    titleEl.textContent = file.label;

    // tabs (only if multiple files)
    tabsEl.innerHTML = _proj.files.length > 1
      ? _proj.files.map((f, i) =>
          `<button class="modal-tab ${i === _fidx ? 'is-active' : ''}" data-fidx="${i}" type="button">${f.label}</button>`
        ).join('')
      : '';

    tabsEl.querySelectorAll('.modal-tab').forEach(btn => {
      btn.addEventListener('click', () => { _fidx = +btn.dataset.fidx; render(); });
    });

    // body content
    bodyEl.innerHTML = '';

    if (type === 'pdf') {
      // embed PDF — works on GitHub Pages (same origin)
      const wrap = document.createElement('div');
      wrap.className = 'viewer-pdf-wrap';

      const iframe = document.createElement('iframe');
      iframe.src   = file.path;
      iframe.title = file.label;
      iframe.setAttribute('allowfullscreen', '');
      wrap.appendChild(iframe);
      bodyEl.appendChild(wrap);

    } else if (type === 'img') {
      const wrap = document.createElement('div');
      wrap.className = 'viewer-img-wrap';
      const img = document.createElement('img');
      img.src = file.path;
      img.alt = file.label;
      wrap.appendChild(img);
      bodyEl.appendChild(wrap);

    } else if (type === 'py') {
      // fetch .py and render with highlight
      bodyEl.innerHTML = `<div class="viewer-loading"><span class="terminal-line">$ carregando ${file.label}…</span></div>`;

      fetch(file.path)
        .then(r => {
          if (!r.ok) throw new Error('HTTP ' + r.status + ' — arquivo não encontrado');
          return r.text();
        })
        .then(code => {
          bodyEl.innerHTML = '';
          const wrap = document.createElement('div');
          wrap.className = 'viewer-py-wrap';

          // fake window bar
          wrap.innerHTML = `
            <div class="py-bar">
              <span class="wdot wdot-r"></span>
              <span class="wdot wdot-y"></span>
              <span class="wdot wdot-g"></span>
              <span class="py-bar-name">${file.label}</span>
              <span class="py-bar-lang">Python</span>
            </div>`;

          const pre  = document.createElement('pre');
          pre.className = 'py-pre';
          const code_el = document.createElement('code');
          code_el.className = 'py-code';
          // set as text first, then highlight
          code_el.textContent = code;
          pre.appendChild(code_el);
          wrap.appendChild(pre);
          bodyEl.appendChild(wrap);
          highlightPy(code_el);
        })
        .catch(err => {
          bodyEl.innerHTML = `<div class="viewer-error">
            <p class="terminal-line">$ erro: ${err.message}</p>
            <p style="margin-top:.8rem;color:var(--text-secondary)">
              Verifique se <code>${file.path}</code> está na pasta <code>arquivos/</code> do repositório.
            </p>
          </div>`;
        });

    } else {
      bodyEl.innerHTML = `<div class="viewer-error">
        <p>Tipo de arquivo não suportado para visualização.</p>
        <a href="${file.path}" target="_blank" rel="noopener noreferrer" class="btn btn-ghost" style="margin-top:1rem;display:inline-flex">
          Abrir em nova aba ↗
        </a>
      </div>`;
    }
  }

  /* ---------- minimal Python syntax highlight ---------- */
  function highlightPy(el) {
    const KW = ['False','None','True','and','as','assert','async','await','break',
      'class','continue','def','del','elif','else','except','finally','for','from',
      'global','if','import','in','is','lambda','nonlocal','not','or','pass',
      'raise','return','try','while','with','yield','self','print','input','len',
      'range','type','int','str','float','list','dict','set','tuple','bool'];

    // work on raw text, build highlighted HTML
    let src = el.textContent;
    // We'll do a simple line-by-line pass to be safe
    const lines = src.split('\n');
    const out = lines.map(line => {
      // escape HTML entities
      let s = line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

      // triple-quoted strings are not handled here (keep simple)
      // single-line strings  "…" or '…'
      s = s.replace(/("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g,
        m => `<span class="py-str">${m}</span>`);

      // comment (only if not inside a string span already — simple heuristic: after first #)
      s = s.replace(/(#.*)$/, m => `<span class="py-cmt">${m}</span>`);

      // numbers
      s = s.replace(/\b(\d+\.?\d*)\b/g, m => `<span class="py-num">${m}</span>`);

      // keywords — skip inside already-tagged spans
      KW.forEach(kw => {
        s = s.replace(
          new RegExp('(?<!<[^>]{0,200})\\b(' + kw + ')\\b(?![^<]*>)','g'),
          `<span class="py-kw">$1</span>`
        );
      });

      return s;
    });
    el.innerHTML = out.join('\n');
  }

  /* ---------- event wiring ---------- */

  // clicks on file chips (delegated — chips are created dynamically)
  document.addEventListener('click', e => {
    const chip = e.target.closest('.file-chip');
    if (chip) {
      openModal(+chip.dataset.pidx, +chip.dataset.fidx);
      return;
    }
    // click on overlay backdrop closes modal
    if (e.target === overlay) closeModal();
  });

  closeBtn.addEventListener('click', closeModal);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
  });
})();
