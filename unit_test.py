import json
import region_cache
import pytest

def _write(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")

def test_load_and_get_by_code(tmp_path, monkeypatch):
    p = tmp_path / "region_data.txt"
    regions = [
        {"code": "VALORIA", "name": "Valoria", "description": "x"},
        {"code": "CELESTRA", "name": "Celestra", "description": "y"}
    ]
    _write(p, regions)
    monkeypatch.setattr(region_cache, "REGION_DATA_FILE", str(p))
    region_cache.reload()
    assert region_cache.get_by_code("VALORIA")["name"] == "Valoria"
    assert len(region_cache.get_all()) == 2
    assert region_cache.get_version().startswith("2-")

def test_expand_all_region_data_mixed(tmp_path, monkeypatch):
    p = tmp_path / "region_data.txt"
    regions = [{"code": "VALORIA", "name": "Valoria"}]
    _write(p, regions)
    monkeypatch.setattr(region_cache, "REGION_DATA_FILE", str(p))
    region_cache.reload()
    mixed = ["VALORIA", {"code": "UNKNOWN", "note": "n"}, {"some": "dict"}]
    out = region_cache.expand_all_region_data(mixed)
    # cached VALORIA expanded, UNKNOWN falls back to provided dict, arbitrary dict preserved
    assert any(r.get("code") == "VALORIA" for r in out)
    assert any(r.get("note") == "n" for r in out)
    assert any(r.get("some") == "dict" for r in out)

def test_reload_handles_malformed(tmp_path, monkeypatch):
    p = tmp_path / "region_data.txt"
    p.write_text("not a json", encoding="utf-8")
    monkeypatch.setattr(region_cache, "REGION_DATA_FILE", str(p))
    region_cache.reload()
    assert region_cache.get_all() == []
    assert region_cache.get_version() == ""