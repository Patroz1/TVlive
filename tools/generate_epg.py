import gzip
import shutil
import subprocess
import xml.etree.ElementTree as ET

from common import DATABASE_DIR, ROOT, read_json

CATALOG_JSON = DATABASE_DIR / "catalog.json"

EPG_DIR = ROOT / "epg"
EPG_SOURCE_GZ = EPG_DIR / "source.xml.gz"
EPG_XML = EPG_DIR / "epg.xml"
EPG_XML_GZ = EPG_DIR / "epg.xml.gz"

EPG_SOURCE_URL = "https://epgshare01.online/epgshare01/epg_ripper_IT1.xml.gz"


EPG_ID_OVERRIDES = {
    "TV8.it": "TV8.HD.it",
    "Cielo.it": "cielo.it",
    "SkyTG24.it": "Sky.TG24.it",
    "La7.it": "LA7.HD.it",
    "La5.it": "La.5.it",
    "TwentySeven.it": "27.Twentyseven.it",
    "GamberoRosso.it": "Gambero.Rosso.HD.it",
    "RTL1025.it": "RTL.102.5.HD.it",
    "DeejayTV.it": "Deejay.TV.it",
    "Radio105.it": "Radio.105.it",
    "R101.it": "R101tv.it",
    "RealTime.it": "Real.Time.it",
    "TopCrime.it": "Top.Crime.it",
    "TgCom24.it": "TGCom.it",
    "MediasetExtra.it": "Mediaset.Extra.it",
    "Italia2.it": "Italia.2.it",
    "Cine34.it": "Cine34.it",
    "Rete4.it": "Rete.4.it",
    "Italia1.it": "Italia.1.it",
    "Canale5.it": "Canale.5.it",
    "Giallo.it": "Giallo.TV.it",
    "FoodNetwork.it": "Food.Network.it",
    "DiscoveryChannel.it": "Discovery.Channel.it",
    "DiscoveryTurbo.it": "",
}


def download_epg() -> None:
    EPG_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Scarico EPG da: {EPG_SOURCE_URL}")

    subprocess.run(
        [
            "curl",
            "-L",
            "-A",
            "Mozilla/5.0",
            "-o",
            str(EPG_SOURCE_GZ),
            EPG_SOURCE_URL,
        ],
        check=True,
    )

    print(f"EPG scaricato: {EPG_SOURCE_GZ.relative_to(ROOT)}")


def load_source_tree() -> ET.ElementTree:
    with gzip.open(EPG_SOURCE_GZ, "rb") as source:
        return ET.parse(source)


def get_catalog_epg_ids(catalog: dict) -> dict:
    result = {}

    for channel_name, item in catalog.items():
        epg_id = item.get("epg", "")

        if not epg_id:
            continue

        mapped_epg_id = EPG_ID_OVERRIDES.get(epg_id, epg_id)

        if not mapped_epg_id:
            continue

        result[channel_name] = mapped_epg_id

    return result


def filter_epg(source_tree: ET.ElementTree, wanted_ids: set) -> ET.ElementTree:
    source_root = source_tree.getroot()

    new_root = ET.Element(source_root.tag, source_root.attrib)

    included_channels = 0
    included_programmes = 0

    for child in source_root:
        if child.tag == "channel":
            channel_id = child.attrib.get("id", "")

            if channel_id in wanted_ids:
                new_root.append(child)
                included_channels += 1

    for child in source_root:
        if child.tag == "programme":
            channel_id = child.attrib.get("channel", "")

            if channel_id in wanted_ids:
                new_root.append(child)
                included_programmes += 1

    print(f"Canali EPG inclusi: {included_channels}")
    print(f"Programmi EPG inclusi: {included_programmes}")

    return ET.ElementTree(new_root)


def write_outputs(tree: ET.ElementTree) -> None:
    tree.write(
        EPG_XML,
        encoding="utf-8",
        xml_declaration=True,
    )

    with open(EPG_XML, "rb") as source:
        with gzip.open(EPG_XML_GZ, "wb") as target:
            shutil.copyfileobj(source, target)

    print(f"Creato: {EPG_XML.relative_to(ROOT)}")
    print(f"Creato: {EPG_XML_GZ.relative_to(ROOT)}")


def main() -> None:
    catalog = read_json(CATALOG_JSON)

    epg_ids_by_channel = get_catalog_epg_ids(catalog)
    wanted_ids = set(epg_ids_by_channel.values())

    print(f"Canali nel catalogo con EPG configurato: {len(epg_ids_by_channel)}")

    download_epg()

    source_tree = load_source_tree()
    source_root = source_tree.getroot()

    available_ids = {
        child.attrib.get("id", "")
        for child in source_root
        if child.tag == "channel"
    }

    matched_ids = wanted_ids & available_ids
    missing_ids = wanted_ids - available_ids

    print(f"ID EPG richiesti: {len(wanted_ids)}")
    print(f"ID EPG trovati: {len(matched_ids)}")
    print(f"ID EPG mancanti: {len(missing_ids)}")

    if missing_ids:
        print()
        print("ID EPG mancanti:")
        for epg_id in sorted(missing_ids):
            print(f"- {epg_id}")

    filtered_tree = filter_epg(source_tree, matched_ids)
    write_outputs(filtered_tree)


if __name__ == "__main__":
    main()