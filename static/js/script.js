// =========================
// AUTO BACKEND DETECTION
// =========================
const BACKEND_URL =
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost"
    ? "http://127.0.0.1:5000"
    : "";

// =========================
// INIT
// =========================
const scanBtn = document.getElementById("scanBtn");
const urlInput = document.getElementById("urlInput");

scanBtn.addEventListener("click", scanURL);
urlInput.addEventListener("keydown", e => {
  if (e.key === "Enter") scanURL();
});

// =========================
// MAIN FUNCTION
// =========================
async function scanURL() {

  const url = urlInput.value.trim();

  const box = document.getElementById("resultBox");
  const label = document.getElementById("resultLabel");
  const msg = document.getElementById("resultMsg");

  const safeBrowsing = document.getElementById("safeBrowsing");
  const aiScore = document.getElementById("aiScore");
  const domainAge = document.getElementById("domainAge");

  const features = document.querySelector(".features");

  // ❌ EMPTY CHECK
  if (!url) {
    alert("Please enter a URL");
    return;
  }

  if (!url.startsWith("http")) {
    alert("URL must start with http or https");
    return;
  }

  document.getElementById("resultArea").classList.add("visible");

  // 🔥 RESET FEATURES (important)
  features.classList.remove("show");

  scanBtn.disabled = true;
  scanBtn.innerText = "Scanning...";

  box.className = "result-box analyzing";
  label.innerText = "Analyzing...";
  msg.innerText = "Running security checks...";

  domainAge.innerText = "-";
  safeBrowsing.innerText = "-";
  aiScore.innerText = "-";

  try {

    const res = await fetch(`${BACKEND_URL}/predict`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({url})
    });

    if (!res.ok) throw new Error("Server error");

    const data = await res.json();

    if (data.error) throw new Error(data.error);

    // =========================
    // RESULT STATE
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

    // DOMAIN AGE
    domainAge.innerText = data.domain_age || "Not Available";

    // SAFE BROWSING
    if (data.safe_browsing === "Threat Found") {
      safeBrowsing.innerText = "Blacklisted ❌";
      safeBrowsing.style.color = "#ef4444";
    }
    else {
      if (data.prediction === 2) {
        safeBrowsing.innerText = "Not blacklisted, but detected as suspicious ⚠️";
        safeBrowsing.style.color = "#facc15";
      } else {
        safeBrowsing.innerText = "Not Blacklisted ✅";
        safeBrowsing.style.color = "#22c55e";
      }
    }

    // RISK
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

    // 🔥 SHOW FEATURES AFTER RESULT
    features.classList.add("show");

  } catch (err) {
    console.error("ERROR:", err);

    box.className = "result-box danger";
    label.innerText = "Error";
    msg.innerText = "Server not responding";

    domainAge.innerText = "-";
    safeBrowsing.innerText = "-";
    aiScore.innerText = "-";
  }

  scanBtn.disabled = false;
  scanBtn.innerText = "Scan Now ↗";
}

// NAV ACTIVE
const navLinks = document.querySelectorAll(".nav-links a");

navLinks.forEach(link => {
  link.addEventListener("click", function() {
    navLinks.forEach(l => l.classList.remove("active"));
    this.classList.add("active");
  });
});
