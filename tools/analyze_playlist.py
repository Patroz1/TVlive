from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PLAYLIST = ROOT / "output" / "live-it.m3u"


def main():
    if not OUTPUT_PLAYLIST.exists():
        print(f"File non trovato: {OUTPUT_PLAYLIST}")
        return

    lines = OUTPUT_PLAYLIST.read_text(
        encoding="utf-8",
        errors="replace",
    ).splitlines()

    extinf_count = sum(1 for line in lines if line.startswith("#EXTINF"))

    active_urls = sum(
        1
        for line in lines
        if line.strip()
        and not line.startswith("#")
        and (
            line.startswith("http://")
            or line.startswith("https://")
        )
    )

    commented_urls = sum(
        1
        for line in lines
        if line.startswith("#http://") or line.startswith("#https://")
    )

    drm_lines = sum(
        1
        for line in lines
        if line.startswith("#KODIPROP")
        or line.startswith("#EXT2-X-DRM")
    )

    user_agent_lines = sum(
        1
        for line in lines
        if line.startswith("#EXTVLCOPT")
    )

    print("Analisi playlist generata")
    print("-------------------------")
    print(f"File analizzato: {OUTPUT_PLAYLIST}")
    print(f"Righe totali: {len(lines)}")
    print(f"Canali dichiarati (#EXTINF): {extinf_count}")
    print(f"URL attivi: {active_urls}")
    print(f"URL commentati/nascosti: {commented_urls}")
    print(f"Righe DRM/KODIPROP: {drm_lines}")
    print(f"Righe user-agent: {user_agent_lines}")


if __name__ == "__main__":
    main()