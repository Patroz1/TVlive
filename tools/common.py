import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SOURCE_PLAYLIST = ROOT / "source" / "live-it-source.m3u"

DATABASE_DIR = ROOT / "database"
CHANNELS_JSON = DATABASE_DIR / "channels.json"
ALIASES_JSON = DATABASE_DIR / "aliases.json"
CATALOG_JSON = DATABASE_DIR / "catalog.json"
NORMALIZED_CHANNELS_JSON = DATABASE_DIR / "normalized_channels.json"

OUTPUT_DIR = ROOT / "output"
OUTPUT_PLAYLIST = OUTPUT_DIR / "live-it.m3u"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def read_lines(path: Path) -> list[str]:
    return read_text(path).splitlines()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}

    text = read_text(path).strip()
    if not text:
        return {}

    return json.loads(text)


def write_json(path: Path, data: dict) -> None:
    write_text(
        path,
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
    )


def normalize_spaces(value: str) -> str:
    return " ".join(value.strip().split())