/* ===== iSkohm Robot Club — app.js ===== */

// ===== PYTHON SYNTAX HIGHLIGHTER =====
function highlightPython(code) {
  // Escape HTML first
  code = code
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');

  // We'll process line by line
  const lines = code.split('\n');
  const result = lines.map(line => highlightLine(line));
  return result.join('\n');
}

function highlightLine(line) {
  // Comments (must be first)
  const commentMatch = line.match(/^(.*?)(#.*)$/);
  if (commentMatch) {
    return highlightTokens(commentMatch[1]) + `<span class="cm">${commentMatch[2]}</span>`;
  }
  return highlightTokens(line);
}

function highlightTokens(line) {
  // STEP 1: Save strings as placeholders so keywords don't match inside them
  // (prevents 'class' keyword matching inside class="str" span attributes)
  const saved = [];
  line = line.replace(/('(?:[^'\\]|\\.)*'|"(?:[^"\\]|\\.)*")/g, (m) => {
    const i = saved.length;
    saved.push(`<span class="str">${m}</span>`);
    return `\x00${i}\x00`;
  });

  // STEP 2: Keywords (no span tags in line yet — safe)
  const keywords = ['from', 'import', 'while', 'for', 'if', 'elif', 'else', 'def', 'class',
                    'return', 'True', 'False', 'None', 'and', 'or', 'not', 'in', 'is',
                    'pass', 'break', 'continue', 'global', 'self', 'with', 'as', 'try',
                    'except', 'finally', 'raise', 'lambda', 'yield', 'del', 'assert'];
  keywords.forEach(kw => {
    const re = new RegExp(`\\b(${kw})\\b`, 'g');
    line = line.replace(re, `<span class="kw">$1</span>`);
  });

  // STEP 3: Numbers
  line = line.replace(/\b(\d+\.?\d*)\b/g, `<span class="num">$1</span>`);

  // STEP 4: Function calls
  line = line.replace(/\b([a-z_][a-zA-Z0-9_]*)(\s*\()/g, `<span class="fn">$1</span>$2`);

  // STEP 5: Restore saved strings
  saved.forEach((s, i) => {
    line = line.split(`\x00${i}\x00`).join(s);
  });

  return line;
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
