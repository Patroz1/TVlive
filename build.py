from pathlib import Path
import shutil
import subprocess
import sys


ROOT = Path(__file__).parent.resolve()
PYTHON = sys.executable

OUTPUT_PLAYLIST = ROOT / "output" / "live-it.m3u"
PUBLIC_PLAYLIST = ROOT / "playlist" / "live-it.m3u"

STEPS = [
    ("Estrazione canali", "tools/extract_channels.py"),
    ("Normalizzazione nomi", "tools/normalize_names.py"),
    ("Generazione catalogo", "tools/generate_catalog.py"),
    ("Generazione playlist", "tools/generate_playlist.py"),
    ("Pubblicazione playlist", None),
    ("Analisi playlist", "tools/analyze_playlist.py"),
]


def run_script(title: str, script: str) -> None:
    print()
    print(f"==> {title}")
    print("-" * (len(title) + 4))

    result = subprocess.run(
        [PYTHON, script],
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        print()
        print(f"Errore durante: {title}")
        sys.exit(result.returncode)


def publish_playlist() -> None:
    print()
    print("==> Pubblicazione playlist")
    print("--------------------------")

    if not OUTPUT_PLAYLIST.exists():
        print(f"File mancante: {OUTPUT_PLAYLIST}")
        sys.exit(1)

    PUBLIC_PLAYLIST.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUT_PLAYLIST, PUBLIC_PLAYLIST)

    print(f"Copiata: {OUTPUT_PLAYLIST.relative_to(ROOT)}")
    print(f"Destinazione: {PUBLIC_PLAYLIST.relative_to(ROOT)}")


def main():
    print()
    print("=" * 60)
    print(" TVlive Build System")
    print("=" * 60)

    for title, script in STEPS:
        if script is None:
            publish_playlist()
        else:
            run_script(title, script)

    print()
    print("=" * 60)
    print(" Build completata con successo")
    print("=" * 60)


if __name__ == "__main__":
    main()