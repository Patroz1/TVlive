from common import (
    ALIASES_JSON,
    CHANNELS_JSON,
    NORMALIZED_CHANNELS_JSON,
    normalize_spaces,
    read_json,
    write_json,
)


def apply_alias(name: str, aliases: dict) -> str:
    return aliases.get(name, name)


def main() -> None:
    channels = read_json(CHANNELS_JSON)
    aliases = read_json(ALIASES_JSON)

    normalized = {}

    for original_name, data in channels.items():
        clean_name = normalize_spaces(original_name)
        final_name = apply_alias(clean_name, aliases)

        if final_name not in normalized:
            normalized[final_name] = {
                "source_names": [],
                "duplicates_in_source": 0,
            }

        normalized[final_name]["source_names"].append(original_name)
        normalized[final_name]["duplicates_in_source"] += data.get(
            "duplicates_in_source", 1
        )

    write_json(NORMALIZED_CHANNELS_JSON, normalized)

    print(f"Canali normalizzati: {len(normalized)}")
    print(f"File creato: {NORMALIZED_CHANNELS_JSON.relative_to(NORMALIZED_CHANNELS_JSON.parents[1])}")


if __name__ == "__main__":
    main()