from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


@dataclass(frozen=True)
class ExportPreset:
    name: str
    props: dict[str, Any]


def infer_type(value: str) -> Any:
    s = value.strip()

    # Booleans
    lower = s.lower()
    if lower in ("true", "false"):
        return lower == "true"

    # Integers
    try:
        if "." not in s:
            return int(s)
    except ValueError:
        pass

    # Floats
    try:
        return float(s)
    except ValueError:
        pass

    # Fallback: string
    return s


def parse_export_presets(xml_path: str | Path) -> list[ExportPreset]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    if root.tag != "exportPresets":
        raise ValueError(f"Expected root <exportPresets>, got <{root.tag}>")

    presets: list[ExportPreset] = []

    for preset_el in root.findall("preset"):
        name = preset_el.get("name")
        if not name:
            raise ValueError("A <preset> is missing its 'name' attribute")

        props: dict[str, Any] = {}
        for prop_el in preset_el.findall("property"):
            key = prop_el.get("name")
            raw = prop_el.get("value")

            if key is None or raw is None:
                raise ValueError("<property> must have both 'name' and 'value' attributes")

            props[key] = infer_type(raw)

        presets.append(ExportPreset(name=name, props=props))

    if not presets:
        raise ValueError("No <preset> elements found")

    return presets