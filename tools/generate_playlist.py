from common import (
    CATALOG_JSON,
    OUTPUT_PLAYLIST,
    SOURCE_PLAYLIST,
    read_json,
    read_lines,
    write_text,
    normalize_spaces,
)


GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/Patroz1/TVlive/main/"
EPG_URL = GITHUB_RAW_BASE_URL + "epg/epg.xml.gz"


WLTV_DISCOVERY_CHANNELS = {
    "NOVE": "Nove",
    "Nove": "Nove",
    "Real Time": "RealTime",
    "Discovery Channel": "Discovery",
    "DMAX": "DMAX",
    "Giallo": "Giallo",
    "Discovery Turbo": "Turbo",
    "Motor Trend": "Turbo",
    "HGTV": "HGTV",
    "HGTV - Home&Garden": "HGTV",
    "Food Network": "FoodNetwork",
}


def extract_channel_name(extinf_line):
    if "," not in extinf_line:
        return ""

    return normalize_spaces(extinf_line.rsplit(",", 1)[1])


def parse_source_blocks(lines):
    blocks = {}
    current_name = None
    current_block = []

    def save_current_block():
        if not current_name or not current_block:
            return

        blocks.setdefault(current_name, []).append(current_block.copy())

    for line in lines:
        if line.startswith("#EXTINF"):
            save_current_block()
            current_name = extract_channel_name(line)
            current_block = [line]
            continue

        if current_name:
            current_block.append(line)

    save_current_block()

    return blocks


def is_playable_line(line):
    stripped = line.strip()

    return (
        stripped.startswith("http://")
        or stripped.startswith("https://")
        or stripped.startswith("plugin://")
    )


def has_playable_line(block):
    for line in block[1:]:
        if is_playable_line(line):
            return True

    return False


def clean_block_lines(block):
    cleaned = []

    for line in block[1:]:
        stripped = line.strip()

        if stripped == "--":
            continue

        if not stripped:
            continue

        cleaned.append(line)

    return cleaned


def choose_best_block(blocks):
    for block in blocks:
        if has_playable_line(block):
            return block

    if blocks:
        return blocks[0]

    return None


def sort_key(item):
    name, data = item
    group = data.get("group") or "99 | Archivio"
    lcn = data.get("lcn")

    if lcn is None:
        lcn = 9999

    return group, lcn, name.lower()


def build_logo_url(logo_path):
    if not logo_path:
        return ""

    if logo_path.startswith("http://") or logo_path.startswith("https://"):
        return logo_path

    return GITHUB_RAW_BASE_URL + logo_path.lstrip("/")


def build_extinf(name, data):
    tvg_id = data.get("epg") or name
    tvg_name = name
    tvg_logo = build_logo_url(data.get("logo") or "")
    group = data.get("group") or "99 | Archivio"
    lcn = data.get("lcn")

    attributes = [
        'tvg-id="' + str(tvg_id) + '"',
        'tvg-name="' + str(tvg_name) + '"',
    ]

    if lcn is not None:
        attributes.append('tvg-chno="' + str(lcn) + '"')

    if tvg_logo:
        attributes.append('tvg-logo="' + str(tvg_logo) + '"')

    attributes.append('group-title="' + str(group) + '"')

    return "#EXTINF:-1 " + " ".join(attributes) + "," + name


def is_wltv_discovery_channel(name):
    return name in WLTV_DISCOVERY_CHANNELS


def build_wltv_discovery_url(name):
    channel = WLTV_DISCOVERY_CHANNELS[name]
    return f"plugin://plugin.video.wltvhelper/play/discovery/{channel}"


def generate_playlist():
    source_lines = read_lines(SOURCE_PLAYLIST)
    catalog = read_json(CATALOG_JSON)
    source_blocks = parse_source_blocks(source_lines)

    output_lines = [f'#EXTM3U x-tvg-url="{EPG_URL}"']

    stats = {
        "catalog_channels": len(catalog),
        "written_channels": 0,
        "playable_channels": [],
        "not_playable_channels": [],
        "missing_source": [],
        "disabled": [],
        "without_playable_url": [],
        "wltv_discovery_channels": [],
    }

    for name, data in sorted(catalog.items(), key=sort_key):
        if not data.get("enabled", True):
            stats["disabled"].append(name)
            continue

        if is_wltv_discovery_channel(name):
            output_lines.append("")
            output_lines.append(build_extinf(name, data))
            output_lines.append(build_wltv_discovery_url(name))

            stats["written_channels"] += 1
            stats["playable_channels"].append(name)
            stats["wltv_discovery_channels"].append(name)
            continue

        aliases = data.get("aliases", [])
        candidates = [name] + aliases

        source_block = None

        for candidate in candidates:
            if candidate in source_blocks:
                source_block = choose_best_block(source_blocks[candidate])
                break

        if not source_block:
            stats["missing_source"].append(name)
            stats["not_playable_channels"].append(name)
            continue

        if has_playable_line(source_block):
            stats["playable_channels"].append(name)
        else:
            stats["without_playable_url"].append(name)
            stats["not_playable_channels"].append(name)

        output_lines.append("")
        output_lines.append(build_extinf(name, data))
        output_lines.extend(clean_block_lines(source_block))

        stats["written_channels"] += 1

    return "\n".join(output_lines).strip() + "\n", stats


def print_list(title, values):
    if not values:
        return

    print()
    print(title)
    for value in values:
        print(f"- {value}")


def main():
    playlist, stats = generate_playlist()
    write_text(OUTPUT_PLAYLIST, playlist)

    print(f"Playlist creata: {OUTPUT_PLAYLIST.relative_to(OUTPUT_PLAYLIST.parents[1])}")
    print(f"EPG collegato: {EPG_URL}")
    print(f"Canali nel catalogo: {stats['catalog_channels']}")
    print(f"Canali scritti in playlist: {stats['written_channels']}")
    print(f"Canali riproducibili: {len(stats['playable_channels'])}")
    print(f"Canali non riproducibili: {len(stats['not_playable_channels'])}")
    print(f"Canali disabilitati: {len(stats['disabled'])}")
    print(f"Canali senza sorgente: {len(stats['missing_source'])}")
    print(f"Canali senza URL attivo: {len(stats['without_playable_url'])}")
    print(f"Canali Discovery via WLTV: {len(stats['wltv_discovery_channels'])}")

    print_list("Discovery via WLTV:", stats["wltv_discovery_channels"])
    print_list("Senza sorgente:", stats["missing_source"])
    print_list("Senza URL attivo:", stats["without_playable_url"])


if __name__ == "__main__":
    main()