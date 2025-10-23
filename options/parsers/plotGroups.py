from dataclasses import dataclass
import xml.etree.ElementTree as ET
from pathlib import Path

# Data classes
@dataclass(frozen=True)
class PlotGroup:
    id: int
    name: str
    png_name: str

# Parsers
def parse_plot_groups(xml_path: str | Path) -> list[PlotGroup] | None:
    tree = ET.parse(xml_path)
    root = tree.getroot()
    plot_groups = []

    for pg in root.findall('./plotGroup'):
        pid = pg.get("id")
        name = pg.get("name")
        png_name = pg.get("pngName")

        try:
            pid = int(pid)
        except ValueError:
            raise ValueError(f"Plot group ID '{pid}' is not an integer.")

        plot_groups.append(
            PlotGroup(
                id=pid,
                name=name,
                png_name=png_name
        ))

    if not plot_groups:
        raise ValueError("No plot groups found in the XML file.")

    return plot_groups
