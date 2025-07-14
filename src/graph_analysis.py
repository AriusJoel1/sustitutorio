import argparse
import json
import subprocess
from collections import defaultdict

def collect_edges():
    """
    obtener pares <commit><padre> de git.
    """
    output = subprocess.check_output(
        ['git', 'rev-list', '--all', '--parents'], text=True
    )
    edges = []
    for line in output.splitlines():
        parts = line.split()
        commit = parts[0]
        parents = parts[1:]
        for p in parents:
            edges.append((commit, p))
    return edges

def build_graph(edges):
    dag = defaultdict(set)
    for c, p in edges:
        dag[c].add(p)
    return dag

def compute_metrics(dag):
    """
    densidad de ramas: numero de nodos / |nodos|
    entropia de historia: H= - sumatoria p_i log2 p_i
    critical merge path: camino minimo de merges necesarios para ir de head a la etiqueta v0.0.0
    """
    nodes = set(dag.keys()) | {p for parents in dag.values() for p in parents}
    n_nodes = len(nodes)
    n_edges = sum(len(parents) for parents in dag.values())
    density = n_edges / n_nodes if n_nodes else 0

    # entropia
    import math
    deg_freq = defaultdict(int)
    for c in nodes:
        deg = len(dag.get(c, []))
        deg_freq[deg] += 1
    entropy = -sum(
        (f/n_nodes) * math.log2(f/n_nodes)
        for f in deg_freq.values() if f>0
    )

    # critical merges
    critical = [c for c, parents in dag.items() if len(parents) > 1]

    return {
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        "density": density,
        "entropy": entropy,
        "critical_merges": critical,
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", "-o", required=True,
        help="ruta de salida para metrics.json"
    )
    args = parser.parse_args()
    edges = collect_edges()
    dag = build_graph(edges)
    metrics = compute_metrics(dag)
    with open(args.output, 'w') as f:
        json.dump(metrics, f, indent=2)
    print(f"[OK] metricas guardadas en {args.output}")

if __name__ == "__main__":
    main() 
    