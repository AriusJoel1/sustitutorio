import json
import subprocess
import os
from src.graph_analysis import build_graph, compute_metrics

def test_build_and_metrics(tmp_path, monkeypatch):
    #simulamos arista
    edges = [
        ("c1", "c0"),
        ("c2", "c1"),
        ("c2", "c0"),
    ]
    #nodos aristas y densidad
    dag = build_graph(edges)
    metrics = compute_metrics(dag)
    assert metrics["n_nodes"] == 3
    assert metrics["n_edges"] == 3
    assert metrics["density"] == 1.0
    assert "c2" in metrics["critical_merges"]

