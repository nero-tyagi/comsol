from pathlib import Path
import xml.etree.ElementTree as ET
from dataclasses import dataclass

# Data classes

@dataclass(frozen=True)
class SolElement:
    sol: str
    view: str

@dataclass(frozen=True)
class WorkItem:
    mph_file: str
    regeneratePlots: bool
    sol_elements: list[SolElement]
    plot_group_ids: list[int]
    qualities: list[float]

@dataclass(frozen=True)
class Jobs:
    plot_groups_catalog: dict[int, str]
    work_items: list[WorkItem]

# Parsers

def _as_bool(s: str | None) -> bool:
    return (s or "").strip().lower() in {"true", "1", "yes", "y", "on"}


def _text(e):
    return (e.text or "").strip()


def parse_jobs(xml_path: str | Path) -> Jobs:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Catalog of PlotGroups
    catalog: dict[int, str] = {}
    for pg in root.findall("./plotGroupsCatalog/plotGroup"):
        pid_raw = pg.get("id")
        name = pg.get("name") or ""
        if pid_raw is None:
            raise ValueError("PlotGroup is missing an id")
        try:
            pid = int(pid_raw.strip())
        except ValueError:
            raise ValueError(f"PlotGroup id '{pid_raw}' is not an integer")
        if pid in catalog:
            raise ValueError(f"Duplicate plotGroup id: {pid}")
        catalog[pid] = name

    if not catalog:
        raise ValueError("No plotGroups catalog found in the XML file")

    work_items: list[WorkItem] = []
    for wi in root.findall("./workItems/workItem"):
        raw = wi.findtext("./regeneratePlots", default="false")
        regeneratePlots = _as_bool(raw)
        mph_file = _text(wi.find("./mphFile"))
        if not mph_file:
            raise ValueError("WorkItem is missing an mphFile")

        sol_elements: list[SolElement] = []
        for se in wi.findall("./solElements/solElement"):
            sol = (se.get("sol") or "")
            view = (se.get("view") or "")
            if not sol or not view:
                raise ValueError(f"solElement must have @sol and @view; got sol={sol!r}, view={view!r}")
            sol_elements.append(SolElement(sol, view))
            if not sol_elements:
                raise ValueError("There are not solElements in the WorkItem")

        pg_ids: list[int] = []
        for pgref in wi.findall("./plotGroups/plotGroup"):
            txt = _text(pgref)
            if not txt:
                continue
            try:
                pid = int(txt)
            except ValueError:
                raise ValueError(f"plotGroup id '{txt}' is not an integer")
            if pid not in catalog:
                raise ValueError(f"plotGroup id '{pid}' is not in the PlotGroups catalog")
            pg_ids.append(pid)
        if not pg_ids:
            raise ValueError("There are not plotGroups in the workItem")

        qualities: list[float] = []
        for q in wi.findall("./qualities/quality"):
            txt = _text(q)
            if not txt:
                continue
            try:
                q = float(txt)
            except ValueError:
                raise ValueError(f"quality '{txt}' is not a float")
            qualities.append(q)
        if not qualities:
            qualities = [1]

        work_items.append(WorkItem(
            mph_file=mph_file,
            regeneratePlots=regeneratePlots,
            sol_elements=sol_elements,
            plot_group_ids=pg_ids,
            qualities=qualities
        ))

    if not work_items:
        raise ValueError("There are not workItems in the XML file")

    return Jobs(plot_groups_catalog=catalog, work_items=work_items)

# Expander
def expand_jobs(jobs: Jobs):
    """
    Yields tuples:
      (mph_file, sol_label, view_id, plot_group_id, plot_group_name, quality)
    """
    for wi in jobs.work_items:
        for se in wi.sol_elements:
            for pid in wi.plot_group_ids:
                pg_name = jobs.plot_groups_catalog[pid]
                for q in wi.qualities:
                    yield wi.mph_file, wi.regeneratePlots, se.sol, se.view, pid, pg_name, q