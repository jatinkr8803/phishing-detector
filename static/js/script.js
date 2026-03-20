// script.js

document.addEventListener("DOMContentLoaded", () => {

  const btn = document.getElementById("scanBtn");

  btn.addEventListener("click", scanURL);

  document.getElementById("urlInput").addEventListener("keydown", function(e) {
    if (e.key === "Enter") scanURL();
  });

});

function scanURL() {

  console.log("BUTTON CLICKED ✅");

  const input = document.getElementById('urlInput').value.trim();

  const area = document.getElementById('resultArea');
  const box = document.getElementById('resultBox');
  const label = document.getElementById('resultLabel');
  const msg = document.getElementById('resultMsg');

  const domainAge = document.getElementById('domainAge');
  const safeBrowsing = document.getElementById('safeBrowsing');
  const aiScore = document.getElementById('aiScore');

  if (!input) return;

  // RESET UI
  box.className = 'result-box analyzing';
  label.innerText = "Analyzing...";
  msg.innerText = "Running checks...";
  domainAge.innerText = "-";
  safeBrowsing.innerText = "-";
  aiScore.innerText = "-";
  aiScore.style.color = "#fff";

  area.classList.add("visible");

  fetch('/predict', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ url: input })
  })
  .then(res => res.json())
  .then(data => {

    console.log("Response:", data);

    if (data.error) {
      box.className = 'result-box danger';
      label.innerText = "Error";
      msg.innerText = data.error;
      return;
    }

    // ✅ FINAL RESULT
    if (data.prediction === 1) {
      box.className = 'result-box danger';
      label.innerText = "Phishing Website";
      msg.innerText = "This site is dangerous ⚠️";
    } else {
      box.className = 'result-box safe';
      label.innerText = "Safe Website";
      msg.innerText = "This site looks safe ✅";
    }

    // ✅ DOMAIN AGE
    domainAge.innerText = data.domain_age || "Not Available";

    // ✅ SAFE BROWSING
    safeBrowsing.innerText = data.safe_browsing || "Unknown";

    // ✅ 🔥 CLEAN PHISHING RISK (NO NUMBERS)
    if (data.ai_score !== undefined) {

      let score = data.ai_score;
      let riskLabel = "";

      // 🎯 If final result is SAFE → always Low
      if (data.prediction === 0) {
        riskLabel = "Low ✅";
        aiScore.style.color = "#22c55e";
      } else {
        if (score < 30) {
          riskLabel = "Low ✅";
          aiScore.style.color = "#22c55e";
        } else if (score < 70) {
          riskLabel = "Medium ⚠️";
          aiScore.style.color = "#facc15";
        } else {
          riskLabel = "High ❌";
          aiScore.style.color = "#ef4444";
        }
      }

      aiScore.innerText = riskLabel;

    } else {
      aiScore.innerText = "N/A";
    }

  })
  .catch((err) => {
    console.error(err);
    box.className = 'result-box danger';
    label.innerText = "Error";
    msg.innerText = "Server not responding";
  });
}