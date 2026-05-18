from pathlib import Path
import pandas as pd

WORKSPACE = Path("workspace").resolve()


def _safe_path(path: str) -> Path:
    """Resolve path and prevent escaping workspace."""
    target = (WORKSPACE / path).resolve()
    if not str(target).startswith(str(WORKSPACE)):
        raise ValueError("Access outside workspace is not allowed")
    return target


def analyze_csv(path: str) -> str:
    """Analyze CSV data statistics."""
    target = _safe_path(path)
    df = pd.read_csv(target)
    return (
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nColumn names: {list(df.columns)}\n"
        f"Missing values:\n{df.isnull().sum().to_string()}\n\nNumerical statistics:\n{df.describe().to_string()}"
    )


def analyze_excel(path: str) -> str:
    """Analyze Excel data statistics."""
    target = _safe_path(path)
    df = pd.read_excel(target)
    return (
        f"Rows: {df.shape[0]}\nColumns: {df.shape[1]}\nColumn names: {list(df.columns)}\n"
        f"Missing values:\n{df.isnull().sum().to_string()}\n\nNumerical statistics:\n{df.describe().to_string()}"
    )
