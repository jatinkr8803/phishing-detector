document.addEventListener("DOMContentLoaded", function () {

  async function scanURL() {
    const url = document.getElementById('urlInput').value.trim();

    if (!url) {
      alert('Please enter a URL');
      return;
    }

    // Loading state
    document.getElementById('domainAge').textContent = 'Checking...';
    document.getElementById('safeBrowsing').textContent = 'Checking...';
    document.getElementById('aiResult').textContent = 'Analyzing...';
    document.getElementById('scanStatus').textContent = 'Scanning...';

    try {
      const response = await fetch("/analyze", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url })
      });

      if (!response.ok) {
        throw new Error("Server error");
      }

      const data = await response.json();

      if (data.error) {
        throw new Error(data.error);
      }

      // -------------------------------
      // UPDATE UI
      // -------------------------------

      document.getElementById('domainAge').textContent =
        data.domain_age_days > 0
          ? data.domain_age_days + " days"
          : "Unavailable";

      document.getElementById('safeBrowsing').textContent =
        data.safe_browsing;

      document.getElementById('aiResult').textContent =
        data.prediction;

      // -------------------------------
      // 🔥 FIXED LOGIC
      // -------------------------------

      const isDanger =
        data.prediction === "Phishing" ||
        data.prediction === "Suspicious";

      document.getElementById('scanStatus').textContent =
        isDanger ? "⚠️ Threat Found" : "✅ No Threat Found";

      // Banner
      if (isDanger) {
        document.getElementById('bannerTitle').textContent =
          "⚠️ This URL is NOT SAFE";
        document.getElementById('bannerDesc').textContent =
          "Potential phishing or suspicious website detected";
        document.getElementById('resultBanner').style.background = "#ffebee";
      } else {
        document.getElementById('bannerTitle').textContent =
          "✅ This URL is SAFE";
        document.getElementById('bannerDesc').textContent =
          "No phishing detected";
        document.getElementById('resultBanner').style.background = "#e8f5e9";
      }

    } catch (error) {
      console.error("ERROR:", error);

      document.getElementById('scanStatus').textContent = "❌ Error";
      document.getElementById('aiResult').textContent = "Failed";
      document.getElementById('safeBrowsing').textContent = "Error";
      document.getElementById('domainAge').textContent = "Error";

      document.getElementById('bannerTitle').textContent =
        "❌ Error analyzing URL";
      document.getElementById('bannerDesc').textContent =
        "Server is not responding or crashed";

      document.getElementById('resultBanner').style.background = "#fff3e0";

      alert("Error connecting to server");
    }
  }

  window.scanURL = scanURL;

  document.getElementById('urlInput').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') scanURL();
  });

});