const BACKEND_URL = "http://127.0.0.1:5000";

// INIT
document.getElementById("scanBtn").addEventListener("click", scanURL);

document.getElementById("urlInput").addEventListener("keydown", function(e) {
  if (e.key === "Enter") scanURL();
});

function scanURL() {

  const url = document.getElementById("urlInput").value.trim();

  const box = document.getElementById("resultBox");
  const label = document.getElementById("resultLabel");
  const msg = document.getElementById("resultMsg");

  const safeBrowsing = document.getElementById("safeBrowsing");
  const aiScore = document.getElementById("aiScore");
  const domainAge = document.getElementById("domainAge");

  if (!url) return;

  document.getElementById("resultArea").classList.add("visible");

  box.className = "result-box analyzing";
  label.innerText = "Analyzing...";
  msg.innerText = "Running checks...";

  fetch(`${BACKEND_URL}/predict`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({url})
  })
  .then(res => res.json())
  .then(data => {

    // =========================
    // FINAL RESULT (3 STATES)
    // =========================
    if (data.prediction === 1) {
      box.className = "result-box danger";
      label.innerText = "Phishing Website";
      msg.innerText = "Blacklisted or dangerous ❌";
    }
    else if (data.prediction === 2) {
      box.className = "result-box warning";
      label.innerText = "Suspicious Website";
      msg.innerText = "New or untrusted domain ⚠️";
    }
    else {
      box.className = "result-box safe";
      label.innerText = "Safe Website";
      msg.innerText = "This site looks safe ✅";
    }

    // DOMAIN
    domainAge.innerText = data.domain_age;

    // SAFE BROWSING TEXT
    if (data.safe_browsing === "Threat Found") {
      safeBrowsing.innerText = "Blacklisted ❌";
      safeBrowsing.style.color = "#ef4444";
    }
    else {
      if (data.prediction === 2) {
        safeBrowsing.innerText = "Not Blacklisted but Suspicious ⚠️";
        safeBrowsing.style.color = "#facc15";
      } else {
        safeBrowsing.innerText = "Not Blacklisted ✅";
        safeBrowsing.style.color = "#22c55e";
      }
    }

    // AI SCORE LABEL (optional)
    if (data.prediction === 1) {
      aiScore.innerText = "High Risk ❌";
      aiScore.style.color = "#ef4444";
    }
    else if (data.prediction === 2) {
      aiScore.innerText = "Medium Risk ⚠️";
      aiScore.style.color = "#facc15";
    }
    else {
      aiScore.innerText = "Low Risk ✅";
      aiScore.style.color = "#22c55e";
    }

  })
  .catch(err => {
    console.error(err);
    box.className = "result-box danger";
    label.innerText = "Error";
    msg.innerText = "Server not responding";
  });
}