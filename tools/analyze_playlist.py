from pathlib import Path

SOURCE = Path("source/live-it-source.m3u")


def main():
    if not SOURCE.exists():
        print(f"File non trovato: {SOURCE}")
        return

    lines = SOURCE.read_text(encoding="utf-8", errors="replace").splitlines()

    extinf_count = sum(1 for line in lines if line.startswith("#EXTINF"))
    url_count = sum(
        1
        for line in lines
        if line.strip()
        and not line.startswith("#")
        and (line.startswith("http://") or line.startswith("https://"))
    )

    commented_urls = sum(
        1
        for line in lines
        if line.startswith("#http://") or line.startswith("#https://")
    )

    print("Analisi playlist")
    print("----------------")
    print(f"Righe totali: {len(lines)}")
    print(f"Canali dichiarati (#EXTINF): {extinf_count}")
    print(f"URL attivi: {url_count}")
    print(f"URL commentati/nascosti: {commented_urls}")


if __name__ == "__main__":
    main()