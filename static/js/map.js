const map = L.map('map', {
  scrollWheelZoom: true,
  zoomControl: true,
  inertia: true,
  worldCopyJump: true
}).setView([20, 0], 2);

map.zoomControl.setPosition('topright');

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://carto.com/">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
}).addTo(map);

// === Severity Icons ===
const iconMap = {
  Critical: L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/1828/1828843.png',
    iconSize: [30, 30],
    iconAnchor: [15, 30],
    popupAnchor: [0, -28]
  }),
  High: L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/190/190406.png',
    iconSize: [28, 28],
    iconAnchor: [14, 28],
    popupAnchor: [0, -26]
  }),
  Medium: L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/252/252035.png',
    iconSize: [26, 26],
    iconAnchor: [13, 26],
    popupAnchor: [0, -24]
  }),
  Low: L.icon({
    iconUrl: 'https://cdn-icons-png.flaticon.com/512/565/565498.png',
    iconSize: [24, 24],
    iconAnchor: [12, 24],
    popupAnchor: [0, -22]
  })
};

const markerCluster = L.markerClusterGroup();
map.addLayer(markerCluster);

// === Main Map Update ===
function updateMap() {
  fetch('/api/threats')
    .then(res => res.json())
    .then(data => {
      const selectedFilter = document.getElementById("filter").value;
      const timeWindow = parseInt(document.getElementById("timeRange").value); // in hours

      markerCluster.clearLayers();
      const feedContainer = document.getElementById("feed");
      feedContainer.innerHTML = "";

      const now = new Date();
      let severityCount = { Critical: 0, High: 0, Medium: 0, Low: 0 };
      let countryCount = {};
      let totalVisible = 0;

      data.forEach(threat => {
        const title = threat.title?.toLowerCase() || "unknown";
        const severity = threat.severity || "Medium";
        const country = threat.country || "Unknown";
        const icon = iconMap[severity] || iconMap["Medium"];
        const source = threat.source || "Unknown";

        // Parse and validate timestamp
        const threatTime = new Date(threat.timestamp);
        if (isNaN(threatTime.getTime())) {
          console.warn("⏳ Skipped due to invalid timestamp:", threat.timestamp);
          return;
        }

        const diffHours = (now - threatTime) / (1000 * 60 * 60);
        if (diffHours > timeWindow) return;

        if (selectedFilter !== "all" && !title.includes(selectedFilter)) return;

        totalVisible++;
        severityCount[severity] = (severityCount[severity] || 0) + 1;
        countryCount[country] = (countryCount[country] || 0) + 1;

        const marker = L.marker([threat.lat, threat.lon], { icon })
          .bindPopup(`<b>${threat.title}</b><br>${threat.description}<br><i>${source}</i>`);
        markerCluster.addLayer(marker);

        const div = document.createElement("div");
        div.className = "feed-item";
        div.innerHTML = `
          <strong>🚨 ${threat.title}</strong><br>
          ${threat.description}<br>
          <small>${threatTime.toLocaleString()}</small><br>
          <span class="tag">${source}</span>
        `;
        feedContainer.prepend(div);
      });

      document.getElementById("threat-count").textContent = `🛡️ Total Threats: ${totalVisible}`;
      document.getElementById("last-updated").textContent = `⏱ Last Updated: ${now.toLocaleTimeString()}`;

      document.getElementById("severity-summary").innerHTML = `
        <b>Threat Severity:</b> 
        🔴 Critical: ${severityCount.Critical} |
        🟠 High: ${severityCount.High} |
        🟡 Medium: ${severityCount.Medium} |
        🟢 Low: ${severityCount.Low}
      `;

      const topCountries = Object.entries(countryCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5);

      document.getElementById("country-list").innerHTML = topCountries
        .map(([country, count]) => `<li>🌍 ${country}: ${count}</li>`)
        .join('');
    })
    .catch(err => console.error("❌ Error updating map:", err));
}

// === Listeners ===
document.getElementById("filter").addEventListener("change", updateMap);
document.getElementById("timeRange").addEventListener("change", updateMap);

// === Start ===
updateMap();
setInterval(updateMap, 10000);
