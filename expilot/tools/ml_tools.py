import json
from pathlib import Path
from typing import Any, Dict


def summarize_json_metrics(path: str) -> str:
    """Read and summarize a JSON metrics file from an ML experiment."""
    file = Path(path)
    if not file.exists():
        return f"Metrics file not found: {path}"

    data: Dict[str, Any] = json.loads(file.read_text(encoding="utf-8"))

    lines = ["=== Experiment Metrics Summary ==="]
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"\n[{key}]")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        elif isinstance(value, list):
            lines.append(f"\n[{key}] ({len(value)} entries)")
            for i, item in enumerate(value[:5]):
                lines.append(f"  [{i}] {item}")
            if len(value) > 5:
                lines.append(f"  ... and {len(value) - 5} more")
        else:
            lines.append(f"  {key}: {value}")

    return "\n".join(lines)


def compare_experiment_results(path_a: str, path_b: str) -> str:
    """Compare two experiment result JSON files and highlight differences."""
    pa, pb = Path(path_a), Path(path_b)
    if not pa.exists():
        return f"File not found: {path_a}"
    if not pb.exists():
        return f"File not found: {path_b}"

    data_a = json.loads(pa.read_text(encoding="utf-8"))
    data_b = json.loads(pb.read_text(encoding="utf-8"))

    lines = ["=== Experiment Comparison ===", f"File A: {pa.name}", f"File B: {pb.name}", ""]

    all_keys = set(list(data_a.keys()) + list(data_b.keys()))
    for key in sorted(all_keys):
        va = data_a.get(key)
        vb = data_b.get(key)

        if va == vb:
            lines.append(f"  {key}: {va} (identical)")
        else:
            lines.append(f"  {key}:")
            lines.append(f"    A: {va}")
            lines.append(f"    B: {vb}")

    return "\n".join(lines)


def generate_experiment_report(path: str) -> str:
    """Generate a Markdown report from experiment metrics JSON."""
    file = Path(path)
    if not file.exists():
        return f"Metrics file not found: {path}"

    data = json.loads(file.read_text(encoding="utf-8"))

    lines = ["# Experiment Report", ""]

    # Table header
    if isinstance(data, dict):
        # Separate scalar and nested values
        scalars = {}
        nested = {}
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                nested[k] = v
            else:
                scalars[k] = v

        if scalars:
            lines.append("## Key Metrics")
            lines.append("")
            lines.append("| Metric | Value |")
            lines.append("|--------|-------|")
            for k, v in scalars.items():
                lines.append(f"| {k} | {v} |")
            lines.append("")

        for section, content in nested.items():
            lines.append(f"## {section}")
            lines.append("")
            if isinstance(content, dict):
                lines.append("| Key | Value |")
                lines.append("|-----|-------|")
                for k, v in content.items():
                    lines.append(f"| {k} | {v} |")
            elif isinstance(content, list):
                for i, item in enumerate(content[:10]):
                    lines.append(f"{i+1}. {item}")
                if len(content) > 10:
                    lines.append(f"\n... and {len(content) - 10} more entries")
            lines.append("")

    return "\n".join(lines)