/* ===== iSkohm Robot Club — app.js ===== */

// ===== PYTHON SYNTAX HIGHLIGHTER (token-based, no regex-on-HTML) =====
const PY_KEYWORDS = new Set(['False','None','True','and','as','assert','break','class',
  'continue','def','del','elif','else','except','finally','for','from','global','if',
  'import','in','is','lambda','not','or','pass','raise','return','try','while','with','yield']);

function esc(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function highlightPython(code) {
  let out = '';
  let i = 0;
  const n = code.length;

  while (i < n) {
    const ch = code[i];

    // Comment
    if (ch === '#') {
      let j = i;
      while (j < n && code[j] !== '\n') j++;
      out += `<span class="cm">${esc(code.slice(i, j))}</span>`;
      i = j;
      continue;
    }

    // String (single or double quote, with escape support)
    if (ch === "'" || ch === '"') {
      const q = ch;
      let j = i + 1;
      while (j < n && code[j] !== q) {
        if (code[j] === '\\') j++;
        j++;
      }
      j++; // closing quote
      out += `<span class="str">${esc(code.slice(i, j))}</span>`;
      i = j;
      continue;
    }

    // Number (only at word boundary — previous char is not alphanumeric/_)
    if (/\d/.test(ch) && (i === 0 || !/[\w]/.test(code[i - 1]))) {
      let j = i;
      while (j < n && /[\d.]/.test(code[j])) j++;
      out += `<span class="num">${esc(code.slice(i, j))}</span>`;
      i = j;
      continue;
    }

    // Word: keyword, function call, or plain identifier
    if (/[a-zA-Z_]/.test(ch)) {
      let j = i;
      while (j < n && /\w/.test(code[j])) j++;
      const word = code.slice(i, j);
      // Look past whitespace for '('
      let k = j;
      while (k < n && code[k] === ' ') k++;
      const isFn = code[k] === '(';

      if (PY_KEYWORDS.has(word)) {
        out += `<span class="kw">${esc(word)}</span>`;
      } else if (isFn) {
        out += `<span class="fn">${esc(word)}</span>`;
      } else if (/^[A-Z]/.test(word)) {
        out += `<span class="cls">${esc(word)}</span>`;
      } else {
        out += esc(word);
      }
      i = j;
      continue;
    }

    // Everything else
    out += esc(ch);
    i++;
  }

  return out;
}

function applyHighlighting() {
  document.querySelectorAll('code.python').forEach(block => {
    const raw = block.textContent;
    block.innerHTML = highlightPython(raw);
  });
}

function applyHighlighting() {
  document.querySelectorAll('code.python').forEach(block => {
    const raw = block.textContent;
    block.innerHTML = highlightPython(raw);
  });
}

// ===== COPY BUTTON =====
function setupCopyButtons() {
  document.querySelectorAll('.copy-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const block = btn.closest('.code-block');
      const code = block.querySelector('code');
      navigator.clipboard.writeText(code.textContent).then(() => {
        btn.textContent = '✓ Copié !';
        btn.style.color = 'var(--green)';
        setTimeout(() => {
          btn.textContent = 'Copier';
          btn.style.color = '';
        }, 2000);
      });
    });
  });
}

// ===== READING PROGRESS BAR =====
function setupProgressBar() {
  const bar = document.querySelector('.progress-bar');
  if (!bar) return;
  window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
    bar.style.width = pct + '%';
  });
}

// ===== NAV ACTIVE STATE =====
function setActiveNav() {
  const path = window.location.pathname;
  document.querySelectorAll('.nav-links a').forEach(a => {
    if (a.getAttribute('href') && path.includes(a.getAttribute('href').replace('../', '').replace('.html', ''))) {
      a.classList.add('active');
    }
  });
}

// ===== CIRCUIT CANVAS ANIMATION =====
function initCircuitCanvas() {
  const canvas = document.getElementById('circuit-canvas');
  if (!canvas) return;

  const ctx = canvas.getContext('2d');
  let W, H, nodes;

  function resize() {
    W = canvas.width = canvas.offsetWidth;
    H = canvas.height = canvas.offsetHeight;
    if (!nodes) initNodes();
  }

  function initNodes() {
    nodes = Array.from({length: 28}, () => ({
      x: Math.random() * W,
      y: Math.random() * H,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 3 + 1,
    }));
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);

    // Draw connections
    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx*dx + dy*dy);
        if (dist < 160) {
          ctx.beginPath();
          ctx.strokeStyle = `rgba(0,180,216,${0.5 * (1 - dist/160)})`;
          ctx.lineWidth = 0.5;
          // Draw right-angle circuit trace
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }

    // Draw nodes
    nodes.forEach(n => {
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fillStyle = '#00b4d8';
      ctx.fill();

      // Node square
      ctx.strokeStyle = 'rgba(0,180,216,0.4)';
      ctx.lineWidth = 1;
      ctx.strokeRect(n.x - 4, n.y - 4, 8, 8);
    });

    // Update positions
    nodes.forEach(n => {
      n.x += n.vx;
      n.y += n.vy;
      if (n.x < 0 || n.x > W) n.vx *= -1;
      if (n.y < 0 || n.y > H) n.vy *= -1;
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw();
}

// ===== COUNTDOWN TIMER =====
function initCountdown() {
  const els = {
    jours: document.getElementById('cd-jours'),
    heures: document.getElementById('cd-heures'),
    minutes: document.getElementById('cd-minutes'),
    secondes: document.getElementById('cd-secondes'),
  };

  if (!els.jours) return;

  // Set competition date — June 2026 (end of school year)
  const target = new Date('2026-06-15T14:00:00');

  function update() {
    const now = new Date();
    const diff = target - now;
    if (diff <= 0) {
      Object.values(els).forEach(el => el && (el.textContent = '00'));
      return;
    }
    const d = Math.floor(diff / 86400000);
    const h = Math.floor((diff % 86400000) / 3600000);
    const m = Math.floor((diff % 3600000) / 60000);
    const s = Math.floor((diff % 60000) / 1000);
    const pad = n => String(n).padStart(2, '0');
    if (els.jours) els.jours.textContent = pad(d);
    if (els.heures) els.heures.textContent = pad(h);
    if (els.minutes) els.minutes.textContent = pad(m);
    if (els.secondes) els.secondes.textContent = pad(s);
  }

  update();
  setInterval(update, 1000);
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  applyHighlighting();
  setupCopyButtons();
  setupProgressBar();
  setActiveNav();
  initCircuitCanvas();
  initCountdown();
});
