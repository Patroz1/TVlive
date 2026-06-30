import json
from collections import Counter
from pathlib import Path

SOURCE = Path("source/live-it-source.m3u")
DATABASE = Path("database/channels.json")


def extract_channel_name(extinf_line: str) -> str:
    if "," not in extinf_line:
        return ""
    return extinf_line.rsplit(",", 1)[-1].strip()


def main():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)

    lines = SOURCE.read_text(encoding="utf-8", errors="replace").splitlines()

    names = []
    for line in lines:
        line = line.strip()
        if line.startswith("#EXTINF"):
            name = extract_channel_name(line)
            if name:
                names.append(name)

    counts = Counter(names)

    database = {}
    for name in sorted(counts.keys(), key=str.lower):
        database[name] = {
            "enabled": True,
            "lcn": None,
            "group": None,
            "tvg_id": None,
            "tvg_name": name,
            "logo": None,
            "duplicates_in_source": counts[name],
            "notes": ""
        }

    DATABASE.write_text(
        json.dumps(database, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8"
    )

    print(f"Canali totali nel sorgente: {len(names)}")
    print(f"Canali unici: {len(database)}")
    print(f"Database creato: {DATABASE}")

    duplicates = {name: count for name, count in counts.items() if count > 1}
    if duplicates:
        print()
        print("Duplicati trovati:")
        for name, count in sorted(duplicates.items(), key=lambda item: (-item[1], item[0])):
            print(f"- {name}: {count}")


if __name__ == "__main__":
    main()