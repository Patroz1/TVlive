from common import CHANNELS_JSON, DATABASE_DIR, read_json, write_json

CATALOG_JSON = DATABASE_DIR / "catalog.json"


KNOWN_CHANNELS = {
    "Rai 1": {
        "aliases": ["Rai 1", "RAI 1", "Rai1"],
        "provider": "Rai",
        "group": "01 | Nazionali",
        "lcn": 1,
        "epg": "Rai1.it",
        "logo": "logos/rai/rai-1.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Rai 2": {
        "aliases": ["Rai 2", "RAI 2", "Rai2"],
        "provider": "Rai",
        "group": "01 | Nazionali",
        "lcn": 2,
        "epg": "Rai2.it",
        "logo": "logos/rai/rai-2.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Rai 3": {
        "aliases": ["Rai 3", "RAI 3", "Rai3"],
        "provider": "Rai",
        "group": "01 | Nazionali",
        "lcn": 3,
        "epg": "Rai3.it",
        "logo": "logos/rai/rai-3.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Rete 4": {
        "aliases": ["Rete 4", "Rete4", "RETE 4"],
        "provider": "Mediaset",
        "group": "01 | Nazionali",
        "lcn": 4,
        "epg": "Rete4.it",
        "logo": "logos/mediaset/rete-4.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Canale 5": {
        "aliases": ["Canale 5", "Canale5", "CANALE 5"],
        "provider": "Mediaset",
        "group": "01 | Nazionali",
        "lcn": 5,
        "epg": "Canale5.it",
        "logo": "logos/mediaset/canale-5.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Italia 1": {
        "aliases": ["Italia 1", "Italia1", "ITALIA 1"],
        "provider": "Mediaset",
        "group": "01 | Nazionali",
        "lcn": 6,
        "epg": "Italia1.it",
        "logo": "logos/mediaset/italia-1.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "LA7": {
        "aliases": ["LA7", "La7"],
        "provider": "Cairo",
        "group": "01 | Nazionali",
        "lcn": 7,
        "epg": "La7.it",
        "logo": "logos/la7/la7.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "TV8": {
        "aliases": ["TV8", "TV 8"],
        "provider": "Sky",
        "group": "01 | Nazionali",
        "lcn": 8,
        "epg": "TV8.it",
        "logo": "logos/sky/tv8.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Nove": {
        "aliases": ["NOVE", "Nove"],
        "provider": "Warner Discovery",
        "group": "01 | Nazionali",
        "lcn": 9,
        "epg": "Nove.it",
        "logo": "logos/discovery/nove.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "TGCOM24": {
        "aliases": ["TG COM 24", "TGCOM24"],
        "provider": "Mediaset",
        "group": "06 | News",
        "lcn": 51,
        "epg": "TgCom24.it",
        "logo": "logos/mediaset/tgcom24.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Sky TG24": {
        "aliases": ["Sky TG24"],
        "provider": "Sky",
        "group": "06 | News",
        "lcn": 50,
        "epg": "SkyTG24.it",
        "logo": "logos/sky/sky-tg24.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
    "Rai News 24": {
        "aliases": ["Rai News 24"],
        "provider": "Rai",
        "group": "06 | News",
        "lcn": 48,
        "epg": "RaiNews24.it",
        "logo": "logos/rai/rai-news-24.png",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    },
}


def empty_catalog_item(name: str) -> dict:
    return {
        "aliases": [name],
        "provider": "",
        "group": "90 | Da revisionare",
        "lcn": None,
        "epg": "",
        "logo": "",
        "country": "IT",
        "type": "tv",
        "enabled": True,
    }


def build_alias_index() -> dict:
    index = {}

    for canonical_name, data in KNOWN_CHANNELS.items():
        for alias in data.get("aliases", []):
            index[alias] = canonical_name

    return index


def main() -> None:
    channels = read_json(CHANNELS_JSON)
    alias_index = build_alias_index()

    catalog = {}
    unknown = []

    for source_name in sorted(channels.keys(), key=str.lower):
        canonical_name = alias_index.get(source_name, source_name)

        if canonical_name in KNOWN_CHANNELS:
            catalog[canonical_name] = KNOWN_CHANNELS[canonical_name]
        else:
            catalog[canonical_name] = empty_catalog_item(canonical_name)
            unknown.append(canonical_name)

    write_json(CATALOG_JSON, catalog)

    print(f"Catalogo creato: {CATALOG_JSON.relative_to(CATALOG_JSON.parents[1])}")
    print(f"Canali nel catalogo: {len(catalog)}")
    print(f"Canali riconosciuti automaticamente: {len(catalog) - len(unknown)}")
    print(f"Canali da revisionare: {len(unknown)}")

    if unknown:
        print()
        print("Da revisionare:")
        for name in unknown:
            print(f"- {name}")


if __name__ == "__main__":
    main()