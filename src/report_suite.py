import argparse
import json
from typing import List

class CommitStatsService:
    def __init__(self, metrics_path: str):
        with open(metrics_path) as f:
            self.metrics = json.load(f)

    def stats(self) -> str:
        m = self.metrics
        lines = [
            "## statistics",
            f"- Nodes: {m['n_nodes']}",
            f"- Edges: {m['n_edges']}",
            f"- Density: {m['density']:.4f}",
            f"- Entropy: {m['entropy']:.4f}",
            f"- Critical merges: {len(m['critical_merges'])}",
            ""
        ]
        return "\n".join(lines)

class ReleaseNotesService:
    def __init__(self, tag_from: str, tag_to: str):
        self.tag_from = tag_from
        self.tag_to = tag_to

    def notes(self) -> str:
        import subprocess
        cmd = ['git', 'log', '--pretty=format:%h %s', f'{self.tag_from}..{self.tag_to}']
        output = subprocess.check_output(cmd, text=True).splitlines()
        lines = ["## release notes"] + [f"- {l}" for l in output] + [""]
        return "\n".join(lines)

class ChangeLogWriter:
    def __init__(self, release_notes: ReleaseNotesService):
        self.release_notes = release_notes

    def changelog(self) -> str:
        base = self.release_notes.notes()
        # reusar formateo si fuera necesario
        return "## changelog\n" + base

class ReportingSuite:
    def __init__(self,
                 stats_svc: CommitStatsService,
                 notes_svc: ReleaseNotesService,
                 writer: ChangeLogWriter):
        self.stats = stats_svc
        self.notes = notes_svc
        self.writer = writer

    def generate(self, fmt: str, out_path: str):
        parts: List[str] = [
            self.stats.stats(),
            self.notes.notes(),
            self.writer.changelog()
        ]
        report = "\n".join(parts)
        with open(out_path, 'w') as f:
            f.write(report)
        return out_path

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--input", "-i", required=True, help="metrics.json")
    p.add_argument("--format", "-f", default="md", help="md | html")
    p.add_argument("--output", "-o", required=True, help="report file")
    p.add_argument("--tag-from", default="HEAD~1", help="tag o commit inicial")
    p.add_argument("--tag-to", default="HEAD", help="tag o commit final")
    args = p.parse_args()

    stats_svc = CommitStatsService(args.input)
    notes_svc = ReleaseNotesService(args.tag_from, args.tag_to)
    writer = ChangeLogWriter(notes_svc)
    suite = ReportingSuite(stats_svc, notes_svc, writer)
    out = suite.generate(args.format, args.output)
    print(f"[OK] reporte generado en {out}")

if __name__ == "__main__":
    main()
