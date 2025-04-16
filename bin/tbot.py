import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from commands import scan, report

import typer
from commands import scan, report

app = typer.Typer()
app.add_typer(scan.app, name="scan")
app.add_typer(report.app, name="report")

if __name__ == "__main__":
    app()
