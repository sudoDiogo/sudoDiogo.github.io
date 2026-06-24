// ============================================
// MATRIX / BINARY RAIN BACKGROUND
// ============================================
(function initMatrixRain() {
  const canvas = document.getElementById('matrix-bg');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  let columns = [];
  const fontSize = 16;
  let frame = 0;

  function resize() {
    canvas.width  = window.innerWidth;
    canvas.height = window.innerHeight;
    const count = Math.floor(canvas.width / fontSize);
    columns = new Array(count).fill(0).map(() => Math.floor(Math.random() * -50));
  }

  function draw() {
    ctx.fillStyle = 'rgba(7, 11, 18, 0.07)';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    ctx.font = fontSize + 'px JetBrains Mono, monospace';

    for (let i = 0; i < columns.length; i++) {
      const char = Math.random() > 0.5 ? '1' : '0';
      const x = i * fontSize;
      const y = columns[i] * fontSize;
      ctx.fillStyle = Math.random() > 0.975 ? '#00d4ff' : '#00ff9d';
      ctx.fillText(char, x, y);
      if (y > canvas.height && Math.random() > 0.975) columns[i] = 0;
      else columns[i]++;
    }
  }

  function loop() {
    frame++;
    if (frame % 2 === 0) draw();
    requestAnimationFrame(loop);
  }

  window.addEventListener('resize', resize);
  resize();
  if (!prefersReducedMotion) requestAnimationFrame(loop);
  else draw();
})();

// ============================================
// MOBILE NAV TOGGLE
// ============================================
(function initNavToggle() {
  const toggle = document.getElementById('navToggle');
  const links  = document.querySelector('.nav-links');
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
  const navLinks  = document.querySelectorAll('.nav-link');
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
  sections.forEach((s) => observer.observe(s));
})();

// ============================================
// SCROLL REVEAL
// ============================================
function applyReveal(container) {
  const targets = container.querySelectorAll(
    '.project-card, .stack-card, .section-head, .stack-inner > p, .stack-inner > h2'
  );
  targets.forEach((el) => {
    el.classList.add('reveal');
    revealObserver.observe(el);
  });
}

const revealObserver = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        revealObserver.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.1 }
);

// run on static elements immediately
document.querySelectorAll('.section-head, .stack-card, .stack-inner > p, .stack-inner > h2')
  .forEach((el) => { el.classList.add('reveal'); revealObserver.observe(el); });

// ============================================
// FOOTER YEAR
// ============================================
(function setFooterYear() {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();

// ============================================
// PROJECT CARDS — render from PROJECTS array
// ============================================
(function renderProjects() {
  const grid = document.getElementById('projects-grid');
  if (!grid || typeof PROJECTS === 'undefined') return;

  const iconSVG = `
    <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M9 18V5l12-2v13" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      <circle cx="6" cy="18" r="3" stroke="currentColor" stroke-width="1.5"/>
      <circle cx="18" cy="16" r="3" stroke="currentColor" stroke-width="1.5"/>
    </svg>`;

  const fileIconSVG = (type) => type === 'pdf'
    ? `<svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" width="14" height="14">
        <path d="M5 2h7l4 4v12H5V2z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
        <path d="M12 2v4h4M7 11h6M7 14h4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
       </svg>`
    : `<svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg" width="14" height="14">
        <path d="M5 2h7l4 4v12H5V2z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
        <path d="M12 2v4h4M7 9l2 2-2 2M11 13h2" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
       </svg>`;

  function getFileType(path) {
    const ext = path.split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (ext === 'py')  return 'py';
    return 'other';
  }

  function buildFilesHTML(files) {
    if (!files || files.length === 0) return '';
    return `
      <div class="card-files">
        <p class="card-files-label">arquivos</p>
        <div class="card-file-list">
          ${files.map((f, i) => {
            const type = getFileType(f.path);
            return `<button class="file-chip" data-project-idx="${f._pidx}" data-file-idx="${i}" title="Abrir ${f.label}">
              ${fileIconSVG(type)}
              <span>${f.label}</span>
            </button>`;
          }).join('')}
        </div>
      </div>`;
  }

  function buildConceptsHTML(concepts) {
    if (!concepts || concepts.length === 0) return '';
    return `<div class="card-concepts">
      ${concepts.map(c => `<span class="concept-tag">${c}</span>`).join('')}
    </div>`;
  }

  // Tag each file with its project index for lookup on click
  const allProjects = PROJECTS.map((p, pidx) => ({
    ...p,
    files: (p.files || []).map(f => ({ ...f, _pidx: pidx }))
  }));

  grid.innerHTML = '';

  allProjects.forEach((proj, idx) => {
    const hasFiles = proj.files && proj.files.length > 0;
    const isConcluded = proj.status === 'concluído';
    const statusClass = isConcluded ? 'status-pill--done' : '';

    const article = document.createElement('article');
    article.className = 'project-card';
    article.dataset.idx = idx;

    article.innerHTML = `
      <div class="card-top">
        <span class="file-tag">${proj.tag}</span>
        <span class="status-pill ${statusClass}">${proj.status}</span>
      </div>

      <div class="card-body">
        <div class="card-left">
          <div class="card-empty-icon">${iconSVG}</div>
          <h3 class="card-title">${proj.title}</h3>
          <p class="card-text">${proj.desc}</p>
          ${buildFilesHTML(proj.files)}
        </div>

        <div class="card-right">
          <p class="card-tech-label">tecnologias</p>
          <div class="card-tech-list">
            ${(proj.tech || []).map(t => `<span class="tech-badge">${t}</span>`).join('')}
          </div>
          <p class="card-tech-label" style="margin-top:1rem">técnicas</p>
          ${buildConceptsHTML(proj.concepts)}
        </div>
      </div>
    `;

    grid.appendChild(article);
  });

  // store for modal usage
  window._allProjects = allProjects;

  // after render, apply reveal
  applyReveal(grid);
})();

// ============================================
// MODAL — file viewer (PDF + Python)
// ============================================
(function initModal() {
  const overlay  = document.getElementById('modalOverlay');
  const closeBtn = document.getElementById('modalClose');
  const body     = document.getElementById('modalBody');
  const title    = document.getElementById('modalTitle');
  const badge    = document.getElementById('modalBadge');
  const tabsEl   = document.getElementById('modalFileTabs');

  if (!overlay) return;

  let currentFiles = [];
  let currentIdx   = 0;

  function openModal(projectIdx, fileIdx) {
    const proj  = (window._allProjects || [])[projectIdx];
    if (!proj) return;

    currentFiles = proj.files;
    currentIdx   = fileIdx;
    renderModalContent();

    overlay.removeAttribute('hidden');
    document.body.style.overflow = 'hidden';
    closeBtn.focus();
  }

  function closeModal() {
    overlay.setAttribute('hidden', '');
    document.body.style.overflow = '';
    // clear iframe/content to stop PDF rendering
    body.innerHTML = '';
    tabsEl.innerHTML = '';
  }

  function getFileType(path) {
    const ext = path.split('.').pop().toLowerCase();
    if (ext === 'pdf') return 'pdf';
    if (ext === 'py')  return 'py';
    return 'other';
  }

  function renderModalContent() {
    const file = currentFiles[currentIdx];
    if (!file) return;

    const type = getFileType(file.path);

    // title & badge
    title.textContent = file.label;
    badge.textContent = type.toUpperCase();
    badge.className   = 'modal-badge modal-badge--' + type;

    // tabs
    tabsEl.innerHTML = currentFiles.map((f, i) => {
      const t = getFileType(f.path);
      const active = i === currentIdx ? 'active' : '';
      return `<button class="modal-tab ${active}" data-fidx="${i}">${f.label}</button>`;
    }).join('');

    tabsEl.querySelectorAll('.modal-tab').forEach((btn) => {
      btn.addEventListener('click', () => {
        currentIdx = parseInt(btn.dataset.fidx);
        renderModalContent();
      });
    });

    // content
    body.innerHTML = '';

    if (type === 'pdf') {
      const iframe = document.createElement('iframe');
      iframe.src   = file.path + '#toolbar=0&navpanes=0';
      iframe.title = file.label;
      iframe.setAttribute('aria-label', 'Visualizador de PDF: ' + file.label);
      body.appendChild(iframe);

    } else if (type === 'py') {
      body.innerHTML = `<div class="py-loading">
        <span class="terminal-line">$ carregando ${file.label}...</span>
      </div>`;

      fetch(file.path)
        .then((r) => {
          if (!r.ok) throw new Error('Arquivo não encontrado (' + r.status + ')');
          return r.text();
        })
        .then((code) => {
          body.innerHTML = '';
          const wrapper = document.createElement('div');
          wrapper.className = 'py-viewer';

          const header = document.createElement('div');
          header.className = 'py-header';
          header.innerHTML = `
            <div class="py-window-dots">
              <span class="wdot wdot-r"></span>
              <span class="wdot wdot-y"></span>
              <span class="wdot wdot-g"></span>
            </div>
            <span class="py-filename">${file.label}</span>
            <span class="py-lang">Python</span>
          `;

          const pre  = document.createElement('pre');
          const codeEl = document.createElement('code');
          codeEl.textContent = code;
          codeEl.className = 'py-code';
          pre.appendChild(codeEl);
          pre.className = 'py-pre';

          wrapper.appendChild(header);
          wrapper.appendChild(pre);
          body.appendChild(wrapper);

          // minimal syntax highlight
          highlightPython(codeEl);
        })
        .catch((err) => {
          body.innerHTML = `<div class="modal-error">
            <p class="terminal-line">$ erro: ${err.message}</p>
            <p>Verifique se o arquivo <strong>${file.path}</strong> está na pasta <code>arquivos/</code> do repositório.</p>
          </div>`;
        });

    } else {
      body.innerHTML = `<div class="modal-error">
        <p>Tipo de arquivo não suportado para visualização inline.</p>
        <a href="${file.path}" target="_blank" rel="noopener noreferrer" class="btn btn-ghost" style="margin-top:1rem;display:inline-flex">
          Abrir em nova aba
        </a>
      </div>`;
    }
  }

  // ── minimal Python syntax highlighter ──
  function highlightPython(el) {
    const keywords = ['def','class','return','if','elif','else','for','while','in','not','and','or',
                      'import','from','as','try','except','finally','with','pass','break','continue',
                      'lambda','yield','raise','True','False','None','self','print'];
    let html = el.textContent
      // escape HTML first
      .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
      // strings (double & single quote, single-line)
      .replace(/(\"[^\"\\]*(?:\\.[^\"\\]*)*\"|\'[^\'\\]*(?:\\.[^\'\\]*)*\')/g,
               '<span class="py-str">$1</span>')
      // comments
      .replace(/(#.*$)/gm, '<span class="py-comment">$1</span>')
      // numbers
      .replace(/\b(\d+\.?\d*)\b/g, '<span class="py-num">$1</span>');

    // keywords (only outside already-tagged spans — simple approach)
    keywords.forEach(kw => {
      html = html.replace(
        new RegExp(`(?<!<[^>]*)\\b(${kw})\\b(?![^<]*>)`, 'g'),
        '<span class="py-kw">$1</span>'
      );
    });

    el.innerHTML = html;
  }

  // ── event wiring ──
  document.addEventListener('click', (e) => {
    const chip = e.target.closest('.file-chip');
    if (chip) {
      const pidx = parseInt(chip.dataset.projectIdx);
      const fidx = parseInt(chip.dataset.fileIdx);
      openModal(pidx, fidx);
    }
  });

  closeBtn.addEventListener('click', closeModal);

  overlay.addEventListener('click', (e) => {
    if (e.target === overlay) closeModal();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !overlay.hasAttribute('hidden')) closeModal();
  });
})();
