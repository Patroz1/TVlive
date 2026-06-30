from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).parent
PYTHON = sys.executable


STEPS = [
    ("Estrazione canali", "tools/extract_channels.py"),
    ("Analisi playlist", "tools/analyze_playlist.py"),
]


def run_step(title, script):
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
    print("TVlive build")
    print("============")

    for title, script in STEPS:
        run_step(title, script)

    print()
    print("Build completata.")


if __name__ == "__main__":
    main()