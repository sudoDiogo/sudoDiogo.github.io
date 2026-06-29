/* ==============================================
   BUBBLE SORT VISUALIZER
   ============================================== */
(function () {
  const stage    = document.getElementById('sorterStage');
  const sortBtn  = document.getElementById('sortBtn');
  const resetBtn = document.getElementById('resetBtn');
  const speedRange = document.getElementById('speedRange');
  const speedVal   = document.getElementById('speedVal');
  const cmpCount   = document.getElementById('cmpCount');
  const swpCount   = document.getElementById('swpCount');

  if (!stage || !sortBtn) return;

  const BAR_COUNT = 40;
  let arr = [], bars = [];
  let running = false, finished = false;
  let comparisons = 0, swaps = 0;

  // speed map: slider value 1-5 → delay in ms
  const SPEED_MAP = { 1: 220, 2: 100, 3: 42, 4: 16, 5: 4 };
  let delay = SPEED_MAP[3];

  function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

  /* ---- build array ---- */
  function buildArray() {
    arr = Array.from({ length: BAR_COUNT }, () => Math.floor(Math.random() * 90) + 10);
    comparisons = 0; swaps = 0;
    updateStats();
    renderBars();
    finished = false;
    sortBtn.textContent = '▶ iniciar';
    sortBtn.classList.remove('is-running');
  }

  /* ---- render bars from arr ---- */
  function renderBars() {
    stage.innerHTML = '';
    bars = arr.map((v, i) => {
      const bar = document.createElement('div');
      bar.className = 'sorter-bar';
      bar.style.height = v + '%';
      bar.dataset.idx = i;
      stage.appendChild(bar);
      return bar;
    });
  }

  /* ---- update a single bar height ---- */
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

  /* ---- bubble sort with animation ---- */
  async function bubbleSort() {
    const n = arr.length;
    for (let i = 0; i < n - 1 && running; i++) {
      for (let j = 0; j < n - i - 1 && running; j++) {
        // highlight comparing pair
        bars[j].className   = 'sorter-bar is-comparing';
        bars[j+1].className = 'sorter-bar is-comparing';
        comparisons++;
        updateStats();
        await sleep(delay);

        if (arr[j] > arr[j+1]) {
          // highlight swapping
          bars[j].className   = 'sorter-bar is-swapping';
          bars[j+1].className = 'sorter-bar is-swapping';
          await sleep(delay);

          // swap in data and DOM heights
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
      // mark sorted position
      if (bars[n - 1 - i]) bars[n - 1 - i].className = 'sorter-bar is-sorted';
    }
    // mark first bar sorted too (last remaining)
    if (bars[0]) bars[0].className = 'sorter-bar is-sorted';
  }

  /* ---- controls ---- */
  sortBtn.addEventListener('click', async () => {
    if (finished) { buildArray(); return; }

    if (running) {
      // pause
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
      // completed naturally
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

  // init
  buildArray();
})();

/* ==============================================
   PDF.js — renderiza primeira página do PDF
   ============================================== */
(function () {
  const canvas  = document.getElementById('pdf-preview-canvas');
  const loadMsg = document.getElementById('pdf-loading-msg');
  if (!canvas) return;

  // PDF.js precisa ser carregado antes (via CDN no index.html)
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
        const viewport = page.getViewport({ scale: 1.4 });
        canvas.width  = viewport.width;
        canvas.height = viewport.height;

        return page.render({
          canvasContext: canvas.getContext('2d'),
          viewport
        }).promise;
      })
      .then(() => {
        if (loadMsg) loadMsg.style.display = 'none';
      })
      .catch(err => {
        if (loadMsg) loadMsg.innerHTML =
          `<span style="color:var(--text-3);font-size:.8rem">⚠ PDF não encontrado — suba <code>arquivos/12pdf.pdf</code></span>`;
        console.warn('PDF.js:', err);
      });
  }

  tryRender();
})();
