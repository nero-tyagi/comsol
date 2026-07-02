from dataclasses import dataclass
import xml.etree.ElementTree as ET
from pathlib import Path

# Data classes
@dataclass(frozen=True)
class IgnoreList:
    name: str
    ignore: list[str]

@dataclass(frozen=True)
class IgnoreLists:
    lists: list[IgnoreList]

# Parsers
def parse_ignore_lists(xml_path: str | Path) -> IgnoreLists | None:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    ignore_lists = []

    for ig in root.findall('./ignoreList'):
        name = ig.get("name")
        ignore = []
        for i in ig.findall('./ignore'):
            ignore.append(i.text)
        ignore_lists.append(IgnoreList(name, ignore))

    if not ignore_lists:
        return None
    return IgnoreLists(ignore_lists)