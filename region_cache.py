import os
import re
import json
import time
import logging
from typing import List, Dict, Any, Union

LOG = logging.getLogger(__name__)

REGION_DATA_FILE = os.path.join(os.path.dirname(__file__), "region_data.txt")

_region_cache: Dict[str, Dict[str, Any]] = {}
_region_version: str = ""

def _load_region_file() -> None:
    global _region_cache, _region_version
    try:
        with open(REGION_DATA_FILE, "r", encoding="utf-8") as f:
            raw = f.read()
        m = re.search(r"\[.*\]", raw, flags=re.S)
        arr_text = m.group(0) if m else raw
        regions = json.loads(arr_text)
        _region_cache = {r.get("code"): r for r in regions if isinstance(r, dict) and r.get("code")}
        _region_version = f"{len(_region_cache)}-{int(os.path.getmtime(REGION_DATA_FILE))}"
        LOG.info("Loaded %d regions, version=%s", len(_region_cache), _region_version)
    except Exception as e:
        LOG.error("Failed to load region file %s: %s", REGION_DATA_FILE, e)
        _region_cache = {}
        _region_version = ""

# initial load at import
_load_region_file()

def reload() -> None:
    """Force reload region data from file."""
    _load_region_file()

def get_version() -> str:
    return _region_version

def get_all() -> List[Dict[str, Any]]:
    return list(_region_cache.values())

def get_by_code(code: str) -> Union[Dict[str, Any], None]:
    return _region_cache.get(code)

def expand_all_region_data(items: List[Union[str, Dict[str, Any]]]) -> List[Dict[str, Any]]:
    """
    Accepts:
     - list of codes: ["VALORIA", ...]
     - list of {"code": "VALORIA"} or full dicts
    Returns list of full region dicts (from cache or original objects).
    """
    out: List[Dict[str, Any]] = []
    if not items:
        return out
    for x in items:
        try:
            if isinstance(x, str):
                r = _region_cache.get(x)
                if r:
                    out.append(r)
            elif isinstance(x, dict):
                code = x.get("code")
                if code:
                    r = _region_cache.get(code)
                    if r:
                        out.append(r)
                    else:
                        out.append(x)
                else:
                    out.append(x)
        except Exception:
            continue
    return out