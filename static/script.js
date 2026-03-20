
  // Allow Enter key
  document.getElementById('urlInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') scanURL();
  });

  function scanURL() {
    const input = document.getElementById('urlInput').value.trim();
    const area = document.getElementById('resultArea');
    const box = document.getElementById('resultBox');
    const icon = document.getElementById('resultIcon');
    const label = document.getElementById('resultLabel');
    const msg = document.getElementById('resultMsg');

    if (!input) {
      area.classList.remove('visible');
      return;
    }

    // Show analyzing state
    box.className = 'result-box analyzing';
    icon.innerHTML = `<svg class="spin" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#93c5fd" stroke-width="2.5" stroke-linecap="round"><path d="M12 2a10 10 0 0 1 10 10"/></svg>`;
    label.textContent = 'Analyzing…';
    msg.textContent = 'Running security checks on ' + input;
    area.classList.add('visible');

    // Simulate async check
    setTimeout(() => {
      const isSuspicious = checkSuspicious(input);
      if (isSuspicious) {
        box.className = 'result-box danger';
        icon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#f87171" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><circle cx="12" cy="16" r="0.5" fill="#f87171"/></svg>`;
        label.textContent = 'Potentially Dangerous';
        msg.textContent = 'This URL shows signs of phishing or malicious activity. Do not proceed.';
      } else {
        box.className = 'result-box safe';
        icon.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#4ade80" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L4 6v6c0 5.25 3.5 10.15 8 11.5C16.5 22.15 20 17.25 20 12V6z"/><polyline points="9 12 11 14 15 10"/></svg>`;
        label.textContent = 'Appears Safe';
        msg.textContent = 'No immediate threats detected. Still exercise caution on unfamiliar sites.';
      }
    }, 1800);
  }

  function checkSuspicious(url) {
    const suspicious = ['bit.ly','tinyurl','free-gift','login-verify','secure-account',
      'paypa1','faceb00k','amaz0n','update-now','click-here','prize','lucky-winner',
      'verify-account','confirm-identity','.xyz','.tk','.cf','.ga','.ml'];
    const lower = url.toLowerCase();
    return suspicious.some(s => lower.includes(s));
  }
