# Cyber Threat Heatmap

> Real-time visualization of global cyber threats using open-source intelligence (OSINT) feeds.

![map](https://github.com/ramakrishna-j466/cyber-threat-heatmap/assets/preview.png)

---

## Features

- Real-time threat aggregation from:
  - [AbuseIPDB](https://www.abuseipdb.com/)
  - [CVE API (circl.lu)](https://cve.circl.lu/)
  - [AlienVault OTX](https://otx.alienvault.com/)
- Interactive world map powered by Leaflet.js
- Filter threats by type and time window (1h, 3h, 5h, 24h)
- Live feed with severity indicators
- Stores all threat data in JSON for reuse

---

##  Tech Stack

- **Frontend**: HTML + JavaScript + Leaflet.js + CSS
- **Backend**: Flask (Python)
- **APIs Used**: CVE, AbuseIPDB, AlienVault OTX

---

##  Project Structure

cyber-threat-heatmap/
├── app.py # Flask web app
├── fetch_data.py # Aggregates threat data from APIs
├── requirements.txt # Python dependencies
├── static/ # Map JS, CSS, icons
├── templates/ # index.html (Jinja2)
├── data/threats.json # Cached threat data


---

## Installation

git clone https://github.com/ramakrishna-j466/cyber-threat-heatmap.git
cd cyber-threat-heatmap
python -m venv venv
venv\Scripts\activate  # or source venv/bin/activate on Linux/macOS
pip install -r requirements.txt


## Run the App

python fetch_data.py  # Fetch threat data
python app.py         # Start server at http://127.0.0.1:5000




