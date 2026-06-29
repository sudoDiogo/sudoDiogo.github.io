/* ==============================================
   BUBBLE SORT VISUALIZER
   ============================================== */
(function () {
  const stage      = document.getElementById('sorterStage');
  const sortBtn    = document.getElementById('sortBtn');
  const resetBtn   = document.getElementById('resetBtn');
  const speedRange = document.getElementById('speedRange');
  const speedVal   = document.getElementById('speedVal');
  const cmpCount   = document.getElementById('cmpCount');
  const swpCount   = document.getElementById('swpCount');

  if (!stage || !sortBtn) return;

  const BAR_COUNT = 40;
  let arr = [], bars = [];
  let running = false, finished = false;
  let comparisons = 0, swaps = 0;

  const SPEED_MAP = { 1: 220, 2: 100, 3: 42, 4: 16, 5: 4 };
  let delay = SPEED_MAP[3];

  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  function buildArray() {
    arr = Array.from({ length: BAR_COUNT }, () => Math.floor(Math.random() * 90) + 10);
    comparisons = 0; swaps = 0;
    updateStats();
    renderBars();
    finished = false;
    sortBtn.textContent = '▶ iniciar';
    sortBtn.classList.remove('is-running');
  }

  function renderBars() {
    stage.innerHTML = '';
    bars = arr.map((v, i) => {
      const bar = document.createElement('div');
      bar.className = 'sorter-bar';
      bar.style.height = v + '%';
      stage.appendChild(bar);
      return bar;
    });
  }

  function setBar(i, cls) {
    if (!bars[i]) return;
    bars[i].style.height = arr[i] + '%';
    bars[i].className = 'sorter-bar' + (cls ? ' ' + cls : '');
  }

  function clearClass(i) { if (bars[i]) bars[i].className = 'sorter-bar'; }

  function updateStats() {
    if (cmpCount) cmpCount.textContent = comparisons;
    if (swpCount) swpCount.textContent = swaps;
  }

  async function bubbleSort() {
    const n = arr.length;
    for (let i = 0; i < n - 1 && running; i++) {
      for (let j = 0; j < n - i - 1 && running; j++) {
        bars[j].className   = 'sorter-bar is-comparing';
        bars[j+1].className = 'sorter-bar is-comparing';
        comparisons++;
        updateStats();
        await sleep(delay);

        if (arr[j] > arr[j+1]) {
          bars[j].className   = 'sorter-bar is-swapping';
          bars[j+1].className = 'sorter-bar is-swapping';
          await sleep(delay);

          [arr[j], arr[j+1]] = [arr[j+1], arr[j]];
          setBar(j,   'is-swapping');
          setBar(j+1, 'is-swapping');
          swaps++;
          updateStats();
          await sleep(delay);
        }

        clearClass(j);
        clearClass(j+1);
      }
      if (bars[n - 1 - i]) bars[n - 1 - i].className = 'sorter-bar is-sorted';
    }
    if (bars[0]) bars[0].className = 'sorter-bar is-sorted';
  }

  sortBtn.addEventListener('click', async () => {
    if (finished) { buildArray(); return; }

    if (running) {
      running = false;
      sortBtn.textContent = '▶ continuar';
      sortBtn.classList.remove('is-running');
      return;
    }

    running = true;
    sortBtn.textContent = '⏸ pausar';
    sortBtn.classList.add('is-running');

    await bubbleSort();

    if (running) {
      finished = true;
      sortBtn.textContent = '↺ novo array';
      sortBtn.classList.remove('is-running');
    }
    running = false;
  });

  resetBtn.addEventListener('click', () => {
    running = false;
    buildArray();
  });

  speedRange.addEventListener('input', () => {
    const v = +speedRange.value;
    delay = SPEED_MAP[v];
    if (speedVal) speedVal.textContent = v + '×';
  });

  buildArray();
})();

/* ==============================================
   PDF.js — renderiza primeira página nos destaques
   ============================================== */
(function () {
  const canvas  = document.getElementById('pdf-preview-canvas');
  const loadMsg = document.getElementById('pdf-loading-msg');
  if (!canvas) return;

  function tryRender() {
    if (typeof pdfjsLib === 'undefined') {
      setTimeout(tryRender, 200);
      return;
    }

    pdfjsLib.GlobalWorkerOptions.workerSrc =
      'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';

    pdfjsLib.getDocument('arquivos/12pdf.pdf').promise
      .then(pdf => pdf.getPage(1))
      .then(page => {
        // escala para caber na coluna (~360px de largura)
        const desiredWidth = canvas.parentElement
          ? canvas.parentElement.clientWidth - 16
          : 360;
        const unscaled = page.getViewport({ scale: 1 });
        const scale    = desiredWidth / unscaled.width;
        const viewport = page.getViewport({ scale });

        canvas.width  = viewport.width;
        canvas.height = viewport.height;

        return page.render({ canvasContext: canvas.getContext('2d'), viewport }).promise;
      })
      .then(() => {
        if (loadMsg) loadMsg.style.display = 'none';
      })
      .catch(err => {
        if (loadMsg) loadMsg.innerHTML =
          `<span style="color:var(--text-3);font-size:.78rem">⚠ suba <code style="color:var(--cyan)">arquivos/12pdf.pdf</code> para ver a prévia</span>`;
        console.warn('PDF.js destaque:', err.message);
      });
  }

  tryRender();
})();
