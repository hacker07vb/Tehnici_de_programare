import requests

SITES = [
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    return f"https://{host}/{path.lstrip('/')}"


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    r = requests.get(url)
    print(f"Status: {r.status_code}")
    print(f"Content-Type: {r.headers.get('Content-Type')}")


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    try:
        r = requests.get(url, timeout=5)
        return {
            "status": r.status_code,
            "content_type": r.headers.get("Content-Type"),
            "length": len(r.content), 
            "server": r.headers.get("Server", "unknown")
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    rezultate = []
    
    for url in SITES:
        rez = check_site(url)
        rez["url"] = url 
        rezultate.append(rez)
        
    reusite = [r for r in rezultate if r["status"] == 200]
    reusite.sort(key=lambda x: x["length"], reverse=True)
    
    for r in reusite:
        print(f"{r['url']} -> {r['status']}, {r['length']} octeți")
        
    nr_reusite = len(reusite)
    nr_esuate = len(rezultate) - nr_reusite
    print(f"Reuşite: {nr_reusite} | Eşuate: {nr_esuate}")


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    try:
        r = requests.get(url, timeout=5)
        present = []
        missing = []
        
        for antet in SECURITY_HEADERS:
            if antet in r.headers:
                present.append(antet)
            else:
                missing.append(antet)
                
        scor = int((len(present) / len(SECURITY_HEADERS)) * 100)
        
        return {
            "present": present,
            "missing": missing,
            "score": scor
        }
    except requests.RequestException as e:
        return {"status": None, "error": str(e)}


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    incercari_facute = 0
    ultimul_status = None
    ultima_eroare = None
    
    for _ in range(attempts):
        incercari_facute += 1
        try:
            r = requests.get(url, timeout=5)
            ultimul_status = r.status_code
            if r.status_code < 500:
                break
        except requests.RequestException as e:
            ultimul_status = None
            ultima_eroare = str(e)
            
    rezultat = {
        "status": ultimul_status,
        "attempts": incercari_facute
    }
    
    if ultimul_status is None and ultima_eroare:
        rezultat["error"] = ultima_eroare
        
    return rezultat