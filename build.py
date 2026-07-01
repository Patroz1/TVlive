from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).parent
PYTHON = sys.executable

STEPS = [
    ("Estrazione canali", "tools/extract_channels.py"),
    ("Normalizzazione nomi", "tools/normalize_names.py"),
    ("Generazione catalogo", "tools/generate_catalog.py"),
    ("Analisi playlist", "tools/analyze_playlist.py"),
]


def run_step(title: str, script: str) -> None:
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


def main():
    print()
    print("=" * 60)
    print(" TVlive Build System")
    print("=" * 60)

    for title, script in STEPS:
        run_step(title, script)

    print()
    print("=" * 60)
    print(" Build completata con successo")
    print("=" * 60)


if __name__ == "__main__":
    main()