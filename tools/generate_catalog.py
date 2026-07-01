from common import CHANNELS_JSON, DATABASE_DIR, read_json, write_json

CATALOG_JSON = DATABASE_DIR / "catalog.json"


GROUPS = {
    "NAZIONALI": "01 | Nazionali",
    "RAI": "02 | Rai",
    "MEDIASET": "03 | Mediaset",
    "DISCOVERY": "04 | Warner Discovery",
    "SKY": "05 | Sky",
    "NEWS": "06 | News",
    "SPORT": "07 | Sport",
    "BAMBINI": "08 | Bambini",
    "RADIO": "09 | Radio",
    "CULTURA": "10 | Cultura",
    "REGIONALI": "11 | Regionali",
    "FAST": "12 | FAST",
    "INTERNAZIONALI": "13 | Internazionali",
    "REVISIONE": "90 | Da revisionare",
}


KNOWN_CHANNELS = {
    "Rai 1": ("Rai", GROUPS["NAZIONALI"], 1, "Rai1.it", "logos/rai/rai-1.png"),
    "Rai 2": ("Rai", GROUPS["NAZIONALI"], 2, "Rai2.it", "logos/rai/rai-2.png"),
    "Rai 3": ("Rai", GROUPS["NAZIONALI"], 3, "Rai3.it", "logos/rai/rai-3.png"),
    "Rete 4": ("Mediaset", GROUPS["NAZIONALI"], 4, "Rete4.it", "logos/mediaset/rete-4.png"),
    "Canale 5": ("Mediaset", GROUPS["NAZIONALI"], 5, "Canale5.it", "logos/mediaset/canale-5.png"),
    "Italia 1": ("Mediaset", GROUPS["NAZIONALI"], 6, "Italia1.it", "logos/mediaset/italia-1.png"),
    "LA7": ("Cairo", GROUPS["NAZIONALI"], 7, "La7.it", "logos/la7/la7.png"),
    "TV8": ("Sky", GROUPS["NAZIONALI"], 8, "TV8.it", "logos/sky/tv8.png"),
    "NOVE": ("Warner Discovery", GROUPS["NAZIONALI"], 9, "Nove.it", "logos/discovery/nove.png"),

    "Rai 4": ("Rai", GROUPS["RAI"], 21, "Rai4.it", "logos/rai/rai-4.png"),
    "Rai 5": ("Rai", GROUPS["RAI"], 23, "Rai5.it", "logos/rai/rai-5.png"),
    "Rai Movie": ("Rai", GROUPS["RAI"], 24, "RaiMovie.it", "logos/rai/rai-movie.png"),
    "Rai Premium": ("Rai", GROUPS["RAI"], 25, "RaiPremium.it", "logos/rai/rai-premium.png"),
    "Rai Gulp": ("Rai", GROUPS["BAMBINI"], 42, "RaiGulp.it", "logos/rai/rai-gulp.png"),
    "Rai Yoyo": ("Rai", GROUPS["BAMBINI"], 43, "RaiYoyo.it", "logos/rai/rai-yoyo.png"),
    "Rai News 24": ("Rai", GROUPS["NEWS"], 48, "RaiNews24.it", "logos/rai/rai-news-24.png"),
    "Rai Sport + HD": ("Rai", GROUPS["SPORT"], 58, "RaiSport.it", "logos/rai/rai-sport.png"),
    "Rai Storia": ("Rai", GROUPS["CULTURA"], 54, "RaiStoria.it", "logos/rai/rai-storia.png"),
    "Rai Scuola": ("Rai", GROUPS["CULTURA"], 57, "RaiScuola.it", "logos/rai/rai-scuola.png"),
    "Rai 4K (HbbTV)": ("Rai", GROUPS["RAI"], 210, "Rai4K.it", "logos/rai/rai-4k.png"),

    "Iris": ("Mediaset", GROUPS["MEDIASET"], 22, "Iris.it", "logos/mediaset/iris.png"),
    "La 5": ("Mediaset", GROUPS["MEDIASET"], 30, "La5.it", "logos/mediaset/la-5.png"),
    "Cine 34": ("Mediaset", GROUPS["MEDIASET"], 34, "Cine34.it", "logos/mediaset/cine-34.png"),
    "Focus": ("Mediaset", GROUPS["MEDIASET"], 35, "Focus.it", "logos/mediaset/focus.png"),
    "TOPcrime": ("Mediaset", GROUPS["MEDIASET"], 39, "TopCrime.it", "logos/mediaset/topcrime.png"),
    "Boing": ("Mediaset", GROUPS["BAMBINI"], 40, "Boing.it", "logos/mediaset/boing.png"),
    "Cartoonito": ("Mediaset", GROUPS["BAMBINI"], 46, "Cartoonito.it", "logos/mediaset/cartoonito.png"),
    "Italia 2": ("Mediaset", GROUPS["MEDIASET"], 49, "Italia2.it", "logos/mediaset/italia-2.png"),
    "TG COM 24": ("Mediaset", GROUPS["NEWS"], 51, "TgCom24.it", "logos/mediaset/tgcom24.png"),
    "Twenty Seven": ("Mediaset", GROUPS["MEDIASET"], 27, "TwentySeven.it", "logos/mediaset/twenty-seven.png"),
    "Med. Extra": ("Mediaset", GROUPS["MEDIASET"], None, "MediasetExtra.it", "logos/mediaset/mediaset-extra.png"),

    "Cielo": ("Sky", GROUPS["SKY"], 26, "Cielo.it", "logos/sky/cielo.png"),
    "Sky TG24": ("Sky", GROUPS["NEWS"], 50, "SkyTG24.it", "logos/sky/sky-tg24.png"),

    "DMAX": ("Warner Discovery", GROUPS["DISCOVERY"], 52, "DMAX.it", "logos/discovery/dmax.png"),
    "Giallo": ("Warner Discovery", GROUPS["DISCOVERY"], 38, "Giallo.it", "logos/discovery/giallo.png"),
    "Real Time": ("Warner Discovery", GROUPS["DISCOVERY"], 31, "RealTime.it", "logos/discovery/real-time.png"),
    "Food Network": ("Warner Discovery", GROUPS["DISCOVERY"], 33, "FoodNetwork.it", "logos/discovery/food-network.png"),
    "HGTV - Home&Garden": ("Warner Discovery", GROUPS["DISCOVERY"], 56, "HGTV.it", "logos/discovery/hgtv.png"),
    "Discovery Channel": ("Warner Discovery", GROUPS["DISCOVERY"], None, "DiscoveryChannel.it", "logos/discovery/discovery-channel.png"),
    "Discovery Turbo": ("Warner Discovery", GROUPS["DISCOVERY"], None, "DiscoveryTurbo.it", "logos/discovery/discovery-turbo.png"),
    "Frisbee": ("Warner Discovery", GROUPS["BAMBINI"], 44, "Frisbee.it", "logos/discovery/frisbee.png"),
    "K2": ("Warner Discovery", GROUPS["BAMBINI"], 41, "K2.it", "logos/discovery/k2.png"),

    "Gambero Rosso": ("Gambero Rosso", GROUPS["CULTURA"], None, "GamberoRosso.it", "logos/varie/gambero-rosso.png"),
    "3B METEO": ("3B Meteo", GROUPS["NEWS"], None, "3BMeteo.it", "logos/varie/3b-meteo.png"),
    "Deejay TV": ("GEDI", GROUPS["RADIO"], 69, "DeejayTV.it", "logos/radio/deejay-tv.png"),

    "RTL 102.5": ("RTL", GROUPS["RADIO"], 36, "RTL1025.it", "logos/radio/rtl-102-5.png"),
    "R101": ("Mediaset", GROUPS["RADIO"], 67, "R101.it", "logos/radio/r101.png"),
    "Radio 105": ("Mediaset", GROUPS["RADIO"], 66, "Radio105.it", "logos/radio/radio-105.png"),
    "Radio KissKiss": ("Kiss Kiss", GROUPS["RADIO"], None, "RadioKissKiss.it", "logos/radio/radio-kisskiss.png"),
    "Radio Number One": ("Radio Number One", GROUPS["RADIO"], None, "RadioNumberOne.it", "logos/radio/radio-number-one.png"),
    "RDS": ("RDS", GROUPS["RADIO"], None, "RDS.it", "logos/radio/rds.png"),
}


ALIASES = {
    "La7": "LA7",
    "Nove": "NOVE",
    "TGCOM24": "TG COM 24",
    "HGTV": "HGTV - Home&Garden",
}


def slugify(value: str) -> str:
    value = value.lower()
    replacements = {
        " ": "-",
        "'": "",
        ".": "",
        "+": "plus",
        "&": "and",
        "(": "",
        ")": "",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


def make_item(
    name: str,
    provider: str,
    group: str,
    lcn,
    epg: str,
    logo: str,
    channel_data: dict,
) -> dict:
    return {
        "aliases": [name],
        "provider": provider,
        "group": group,
        "lcn": lcn,
        "epg": epg,
        "logo": logo,
        "country": "IT",
        "type": "radio" if group == GROUPS["RADIO"] else "tv",
        "enabled": channel_data.get("enabled", True),
        "source": {
            "tvg_name": channel_data.get("tvg_name", name),
            "duplicates_in_source": channel_data.get("duplicates_in_source", 1),
        },
    }


def make_known_item(name: str, channel_data: dict) -> dict:
    provider, group, lcn, epg, logo = KNOWN_CHANNELS[name]
    return make_item(name, provider, group, lcn, epg, logo, channel_data)


def make_fast_item(name: str, provider: str, channel_data: dict) -> dict:
    slug = slugify(name)
    return make_item(
        name=name,
        provider=provider,
        group=GROUPS["FAST"],
        lcn=None,
        epg="",
        logo=f"logos/fast/{slug}.png",
        channel_data=channel_data,
    )


def make_review_item(name: str, channel_data: dict) -> dict:
    return make_item(
        name=name,
        provider="",
        group=GROUPS["REVISIONE"],
        lcn=None,
        epg="",
        logo="",
        channel_data=channel_data,
    )


def classify_channel(source_name: str, channel_data: dict) -> tuple[str, dict, bool]:
    canonical_name = ALIASES.get(source_name, source_name)

    if canonical_name in KNOWN_CHANNELS:
        return canonical_name, make_known_item(canonical_name, channel_data), True

    upper_name = canonical_name.upper()

    if upper_name.startswith("RAKUTEN"):
        return canonical_name, make_fast_item(canonical_name, "Rakuten TV", channel_data), True

    if upper_name.startswith("CHILI"):
        return canonical_name, make_fast_item(canonical_name, "CHILI", channel_data), True

    if "CINE" in upper_name or "MOVIES" in upper_name or "CINEMA" in upper_name:
        return canonical_name, make_fast_item(canonical_name, "FAST", channel_data), True

    if upper_name in {
        "WESTERN TIME",
        "CRIME TIME",
        "STORIE CRIMINALI",
        "DURI A MORIRE",
        "GLI IMMORTALI",
    }:
        return canonical_name, make_fast_item(canonical_name, "FAST", channel_data), True

    if upper_name.startswith("GF "):
        return canonical_name, make_review_item(canonical_name, channel_data), False

    return canonical_name, make_review_item(canonical_name, channel_data), False


def main() -> None:
    channels = read_json(CHANNELS_JSON)

    catalog = {}
    unknown = []
    recognized = 0

    for source_name in sorted(channels.keys(), key=str.lower):
        channel_data = channels[source_name]
        canonical_name, item, is_recognized = classify_channel(source_name, channel_data)

        catalog[canonical_name] = item

        if is_recognized:
            recognized += 1
        else:
            unknown.append(canonical_name)

    write_json(CATALOG_JSON, catalog)

    print(f"Catalogo creato: {CATALOG_JSON.relative_to(CATALOG_JSON.parents[1])}")
    print(f"Canali nel catalogo: {len(catalog)}")
    print(f"Canali riconosciuti automaticamente: {recognized}")
    print(f"Canali da revisionare: {len(unknown)}")

    if unknown:
        print()
        print("Da revisionare:")
        for name in unknown:
            print(f"- {name}")


if __name__ == "__main__":
    main()