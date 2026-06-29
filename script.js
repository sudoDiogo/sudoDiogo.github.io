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
   ACTIVE NAV ON SCROLL  (corrigido)
   ============================================== */
(function () {
  const sections = document.querySelectorAll('main section[id]');
  const navLinks = document.querySelectorAll('.nav-link');
  if (!sections.length) return;

  const obs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        navLinks.forEach(l =>
          l.classList.toggle('active', l.getAttribute('href') === '#' + e.target.id)
        );
      }
    });
  }, { rootMargin: '-45% 0px -45% 0px' });

  sections.forEach(s => obs.observe(s));
})();

/* ==============================================
   FOOTER YEAR
   ============================================== */
(function () {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();

/* ==============================================
   SCROLL REVEAL
   ============================================== */
const revealObs = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('is-visible');
      revealObs.unobserve(e.target);
    }
  });
}, { threshold: 0.08 });

function enableReveal(root) {
  root.querySelectorAll('.reveal').forEach(el => revealObs.observe(el));
}

document.querySelectorAll('.section-head, .stack-card, .destaque-card').forEach(el => {
  el.classList.add('reveal');
  revealObs.observe(el);
});

/* ==============================================
   PROJECT CARD RENDERER
   ============================================== */
(function () {
  const grid = document.getElementById('projects-grid');
  if (!grid || typeof PROJECTS === 'undefined') return;

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
    if (type === 'txt') return `<svg viewBox="0 0 16 16" fill="none" width="13" height="13">
      <path d="M3 1h7l3 3v11H3V1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M10 1v3h3M5 7h6M5 10h6M5 13h4" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`;
    return `<svg viewBox="0 0 16 16" fill="none" width="13" height="13">
      <path d="M3 1h7l3 3v11H3V1z" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/>
      <path d="M10 1v3h3" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
    </svg>`;
  }

  function fileType(path) {
    const ext = (path || '').split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (ext === 'py')  return 'py';
    if (ext === 'txt') return 'txt';
    if (['png','jpg','jpeg','gif','webp'].includes(ext)) return 'img';
    return 'other';
  }

  grid.innerHTML = '';

  PROJECTS.forEach((proj, pidx) => {
    const hasFiles = proj.files && proj.files.length > 0;
    const done = proj.status === 'Completo';

    const card = document.createElement('article');
    card.className = 'project-card reveal';
    card.dataset.pidx = pidx;

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

  window._PROJECTS = PROJECTS;
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

  let _proj = null;
  let _fidx = 0;

  function openModal(pidx, fidx) {
    const projects = window._PROJECTS;
    if (!projects || !projects[pidx]) return;
    _proj = projects[pidx];
    _fidx = fidx;
    render();
    overlay.classList.add('is-open');
    overlay.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeModal() {
    overlay.classList.remove('is-open');
    overlay.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = '';
    setTimeout(() => { bodyEl.innerHTML = ''; tabsEl.innerHTML = ''; }, 300);
  }

  function ftype(path) {
    const ext = (path || '').split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (ext === 'py')  return 'py';
    if (ext === 'txt') return 'txt';
    if (['png','jpg','jpeg','gif','webp'].includes(ext)) return 'img';
    return 'other';
  }

  function render() {
    const file = _proj.files[_fidx];
    if (!file) return;
    const type = ftype(file.path);

    badgeEl.textContent = type.toUpperCase();
    badgeEl.className   = 'modal-badge modal-badge--' + type;
    titleEl.textContent = file.label;

    tabsEl.innerHTML = _proj.files.length > 1
      ? _proj.files.map((f, i) =>
          `<button class="modal-tab ${i === _fidx ? 'is-active' : ''}" data-fidx="${i}" type="button">${f.label}</button>`
        ).join('')
      : '';

    tabsEl.querySelectorAll('.modal-tab').forEach(btn => {
      btn.addEventListener('click', () => { _fidx = +btn.dataset.fidx; render(); });
    });

    bodyEl.innerHTML = '';

    if (type === 'pdf') {
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
      bodyEl.innerHTML = `<div class="viewer-loading"><span class="terminal-line">$ carregando ${file.label}…</span></div>`;
      fetch(file.path)
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
        .then(code => {
          bodyEl.innerHTML = '';
          const wrap = document.createElement('div');
          wrap.className = 'viewer-py-wrap';
          wrap.innerHTML = `<div class="py-bar">
            <span class="wdot wdot-r"></span><span class="wdot wdot-y"></span><span class="wdot wdot-g"></span>
            <span class="py-bar-name">${file.label}</span>
            <span class="py-bar-lang">Python</span>
          </div>`;
          const pre = document.createElement('pre');
          pre.className = 'py-pre';
          const codeEl = document.createElement('code');
          codeEl.className = 'py-code';
          codeEl.textContent = code;
          pre.appendChild(codeEl);
          wrap.appendChild(pre);
          bodyEl.appendChild(wrap);
          highlightPy(codeEl);
        })
        .catch(err => {
          bodyEl.innerHTML = `<div class="viewer-error">
            <p class="terminal-line">$ erro: ${err.message}</p>
            <p style="margin-top:.8rem">Verifique se <code>${file.path}</code> está na pasta <code>arquivos/</code>.</p>
          </div>`;
        });

    } else if (type === 'txt') {
      bodyEl.innerHTML = `<div class="viewer-loading"><span class="terminal-line">$ carregando ${file.label}…</span></div>`;
      fetch(file.path)
        .then(r => { if (!r.ok) throw new Error('HTTP ' + r.status); return r.text(); })
        .then(text => {
          bodyEl.innerHTML = '';
          const wrap = document.createElement('div');
          wrap.className = 'viewer-py-wrap';
          wrap.innerHTML = `<div class="py-bar">
            <span class="wdot wdot-r"></span><span class="wdot wdot-y"></span><span class="wdot wdot-g"></span>
            <span class="py-bar-name">${file.label}</span>
            <span class="py-bar-lang">Texto</span>
          </div>`;
          const pre = document.createElement('pre');
          pre.className = 'py-pre';
          const codeEl = document.createElement('code');
          codeEl.className = 'py-code';
          codeEl.style.color = 'var(--text-1)';
          codeEl.textContent = text;
          pre.appendChild(codeEl);
          wrap.appendChild(pre);
          bodyEl.appendChild(wrap);
        })
        .catch(err => {
          bodyEl.innerHTML = `<div class="viewer-error">
            <p class="terminal-line">$ erro: ${err.message}</p>
            <p style="margin-top:.8rem">Verifique se <code>${file.path}</code> está na pasta <code>arquivos/</code>.</p>
          </div>`;
        });

    } else {
      bodyEl.innerHTML = `<div class="viewer-error">
        <p>Tipo de arquivo não suportado para visualização inline.</p>
        <a href="${file.path}" target="_blank" rel="noopener noreferrer" class="btn btn-ghost" style="margin-top:1rem;display:inline-flex">
          Abrir em nova aba ↗
        </a>
      </div>`;
    }
  }

  function highlightPy(el) {
    const KW = ['False','None','True','and','as','assert','async','await','break',
      'class','continue','def','del','elif','else','except','finally','for','from',
      'global','if','import','in','is','lambda','nonlocal','not','or','pass',
      'raise','return','try','while','with','yield','self','print','input','len',
      'range','type','int','str','float','list','dict','set','tuple','bool'];
    const lines = el.textContent.split('\n');
    const out = lines.map(line => {
      let s = line.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
      s = s.replace(/("""[\s\S]*?"""|'''[\s\S]*?'''|"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')/g,
        m => `<span class="py-str">${m}</span>`);
      s = s.replace(/(#.*)$/, m => `<span class="py-cmt">${m}</span>`);
      s = s.replace(/\b(\d+\.?\d*)\b/g, m => `<span class="py-num">${m}</span>`);
      KW.forEach(kw => {
        s = s.replace(new RegExp('(?<!<[^>]{0,200})\\b(' + kw + ')\\b(?![^<]*>)','g'),
          `<span class="py-kw">$1</span>`);
      });
      return s;
    });
    el.innerHTML = out.join('\n');
  }

  document.addEventListener('click', e => {
    const chip = e.target.closest('.file-chip');
    if (chip) { openModal(+chip.dataset.pidx, +chip.dataset.fidx); return; }
    if (e.target === overlay) closeModal();
  });

  closeBtn.addEventListener('click', closeModal);

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && overlay.classList.contains('is-open')) closeModal();
  });
})();
