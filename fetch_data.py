import requests
import json
import random
from datetime import datetime, timezone
import time

# === API KEYS ===
ABUSE_API_KEY = "49259e2ea92e602320cd1a076e33a256c2a1e8a8ea1efcb3f988cb258d7faf51423e8d844a5abbcf"
OTX_API_KEY = "89a92ab5f0675177e4bd15fdd11c76201991e10531ec56ac6945410ebd149d2a"

# === Geolocation Helper ===
def get_ip_location(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,lat,lon", timeout=3).json()
        if res["status"] == "success":
            return res["lat"], res["lon"], res["country"]
    except:
        pass
    return None, None, None

# === Severity Helper ===
def get_severity(text):
    text = text.lower()
    if any(x in text for x in ["critical", "apt", "ransomware"]):
        return "Critical"
    elif any(x in text for x in ["high", "exploit", "rat"]):
        return "High"
    elif any(x in text for x in ["brute", "malware", "trojan"]):
        return "Medium"
    return "Low"

# === Fetch from AbuseIPDB ===
def fetch_abuseipdb():
    print("[*] Fetching from AbuseIPDB...")
    threats = []
    try:
        response = requests.get(
            "https://api.abuseipdb.com/api/v2/blacklist?confidenceMinimum=85&limit=50",
            headers={"Key": ABUSE_API_KEY, "Accept": "application/json"},
            timeout=10
        ).json()

        for entry in response.get("data", []):
            ip = entry["ipAddress"]
            lat, lon, country = get_ip_location(ip)
            if lat and lon:
                threats.append({
                    "title": f"Blacklisted IP: {ip}",
                    "description": f"Abuse Score: {entry['abuseConfidenceScore']}, Domain: {entry.get('domain', 'N/A')}",
                    "lat": lat,
                    "lon": lon,
                    "country": country,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "severity": "High",
                    "source": "AbuseIPDB"
                })
    except Exception as e:
        print("[!] AbuseIPDB Error:", e)
    return threats

# === Fetch Latest CVEs ===
def fetch_cve():
    print("[*] Fetching latest CVEs...")
    threats = []
    try:
        res = requests.get("https://cve.circl.lu/api/last", timeout=10).json()
        for cve in res:
            timestamp = cve.get("Published") or datetime.now(timezone.utc).isoformat()
            threats.append({
                "title": cve.get("id", "Unknown CVE"),
                "description": cve.get("summary", "No description provided."),
                "lat": random.uniform(-60, 70),
                "lon": random.uniform(-180, 180),
                "country": "Unknown",
                "timestamp": timestamp,
                "severity": "Medium",
                "source": "CVE API"
            })
    except Exception as e:
        print("[!] CVE API Error:", e)
    return threats

# === Fetch from AlienVault OTX ===
def fetch_otx():
    print("[*] Fetching from AlienVault OTX...")
    threats = []
    try:
        res = requests.get(
            "https://otx.alienvault.com/api/v1/pulses/subscribed",
            headers={"X-OTX-API-KEY": OTX_API_KEY},
            timeout=10
        )
        res.raise_for_status()
        pulses = res.json().get("results", [])

        for pulse in pulses:
            title = pulse.get("name", "Unknown Threat")
            description = pulse.get("description", "")
            timestamp = pulse.get("modified", datetime.now(timezone.utc).isoformat())
            for ind in pulse.get("indicators", []):
                if ind.get("type") == "IPv4":
                    lat, lon, country = get_ip_location(ind["indicator"])
                    if lat and lon:
                        threats.append({
                            "title": title,
                            "description": description,
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "lat": lat,
                            "lon": lon,
                            "country": country,
                            "severity": get_severity(title + " " + description),
                            "source": "AlienVault OTX"
                        })
    except Exception as e:
        print("[!] OTX Error:", e)
    return threats

# === Aggregate and Save All ===
def fetch_all_threats():
    print("🚀 Aggregating threats from multiple sources...\n")
    abuse = fetch_abuseipdb()
    time.sleep(1)
    cve = fetch_cve()
    time.sleep(1)
    otx = fetch_otx()

    all_threats = abuse + cve + otx
    print(f"\n✅ Total threats gathered: {len(all_threats)}")

    with open("data/threats.json", "w") as f:
        json.dump(all_threats, f, indent=2)
        print("💾 Saved to data/threats.json")

if __name__ == "__main__":
    fetch_all_threats()
