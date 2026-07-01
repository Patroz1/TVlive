import json
import re
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SOURCE_FILE = ROOT / "source" / "live-it-source.m3u"
CATALOG_FILE = ROOT / "database" / "catalog.json"

EXTINF_RE = re.compile(r'#EXTINF:[^\n]*,(.+)$')
LOGO_RE = re.compile(r'tvg-logo="([^"]+)"')


def normalize_name(name):
    return (
        name.strip()
        .lower()
        .replace(" hd", "")
        .replace("  ", " ")
    )


def parse_source_logos():
    logos = {}

    with SOURCE_FILE.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()

            if not line.startswith("#EXTINF"):
                continue

            name_match = EXTINF_RE.search(line)
            logo_match = LOGO_RE.search(line)

            if not name_match or not logo_match:
                continue

            name = name_match.group(1).strip()
            logo_url = logo_match.group(1).strip()

            if logo_url.startswith("http"):
                logos[normalize_name(name)] = logo_url

    return logos


def load_catalog():
    with CATALOG_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def download_file(url, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    with urllib.request.urlopen(request, timeout=20) as response:
        data = response.read()

    destination.write_bytes(data)


def main():
    source_logos = parse_source_logos()
    catalog = load_catalog()

    downloaded = 0
    missing = []
    failed = []

    for channel_name, channel in catalog.items():
        logo_path = channel.get("logo")
        aliases = channel.get("aliases", [])

        if not logo_path:
            continue

        candidates = [channel_name] + aliases

        logo_url = None

        for candidate in candidates:
            key = normalize_name(candidate)
            if key in source_logos:
                logo_url = source_logos[key]
                break

        if not logo_url:
            missing.append(channel_name)
            continue

        destination = ROOT / logo_path

        try:
            download_file(logo_url, destination)
            downloaded += 1
            print(f"OK  {channel_name} -> {logo_path}")
        except Exception as e:
            failed.append((channel_name, str(e)))
            print(f"ERR {channel_name}: {e}")

    print()
    print("Download loghi completato")
    print("-------------------------")
    print(f"Loghi scaricati: {downloaded}")
    print(f"Canali senza logo sorgente: {len(missing)}")
    print(f"Errori download: {len(failed)}")

    if missing:
        print()
        print("Senza logo sorgente:")
        for name in missing:
            print(f"- {name}")

    if failed:
        print()
        print("Errori:")
        for name, error in failed:
            print(f"- {name}: {error}")


if __name__ == "__main__":
    main()