import json
import os
import pytest
from src.report_suite import CommitStatsService, ReleaseNotesService, ChangeLogWriter, ReportingSuite

class DummyNotes:
    def notes(self): return "## release notes\n- note\n"

def metrics_file(tmp_path):
    data = {"n_nodes":1,"n_edges":0,"density":0,"entropy":0,"critical_merges":[]}
    path = tmp_path / "metrics.json"
    path.write_text(json.dumps(data))
    return str(path)

def test_commit_stats(metrics_file):
    svc = CommitStatsService(metrics_file)
    out = svc.stats()
    assert "## statistics" in out

@pytest.mark.skipif(
    os.getenv("GIT_LARGE_REPO") == "true",
    reason="Slow on large repos"
)
def test_release_notes(monkeypatch):
    #mock subprocess
    import subprocess
    monkeypatch.setattr(subprocess, "check_output", lambda *args, **kw: "a1 msg")
    svc = ReleaseNotesService("v1.0","v1.1")
    out = svc.notes()
    assert "- a1 msg" in out

def test_full_integration(metrics_file, tmp_path, monkeypatch):
    #creamos suite 
    svc = CommitStatsService(metrics_file)
    notes = DummyNotes()
    writer = ChangeLogWriter(notes)
    suite = ReportingSuite(svc, notes, writer)
    report_path = tmp_path / "r.md"
    suite.generate("md", str(report_path))
    text = report_path.read_text()
    assert "## statistics" in text
    assert "## release notes" in text
    assert "## changelog" in text
