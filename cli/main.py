"""ExperimentPilot CLI — Interactive terminal agent with streaming output."""

import sys
import os

# Ensure project root is on sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import typer
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.text import Text
from expilot.core.agent import AgentEngine
from expilot.i18n import t

app = typer.Typer(help="ExperimentPilot — Visual Multi-Agent Platform (CLI)")
console = Console()

MODES = ["general", "file", "code", "data", "ml", "research"]
MODE_LABELS = {
    "general": "通用助手",
    "file": "文件助手",
    "code": "代码助手",
    "data": "数据分析",
    "ml": "ML实验",
    "research": "研究助手",
}


def print_step(step_info: dict, step_num: int):
    """Print a single step from run_stream with Rich formatting."""
    stype = step_info["type"]

    if stype == "thought":
        console.print(f"  [dim]Step {step_num}:[/dim] {step_info['content'][:100]}")

    elif stype == "tool_call":
        tool = step_info.get("tool_name", "?")
        args = step_info.get("arguments", {})
        args_str = ", ".join(f"{k}={repr(v)[:40]}" for k, v in args.items())
        console.print(f"  [yellow]>[/yellow] [bold]{tool}[/bold]({args_str})")

    elif stype == "observation":
        preview = step_info.get("content", "")
        console.print(f"  [green]<[/green] {preview[:200]}")

    elif stype == "final":
        console.print()
        console.print(Panel(
            Markdown(step_info["content"]),
            title="[bold green]Answer[/bold green]",
            border_style="green",
            padding=(0, 1),
        ))

    elif stype == "error":
        console.print()
        console.print(Panel(
            step_info["content"],
            title="[bold red]Error[/bold red]",
            border_style="red",
        ))


@app.command()
def chat(
    mode: str = typer.Option("general", "-m", "--mode", help=f"Agent mode: {', '.join(MODES)}"),
    max_steps: int = typer.Option(8, "-s", "--steps", help="Max execution steps (3-30)"),
):
    """Start interactive chat with the agent."""
    if mode not in MODES:
        console.print(f"[red]Unknown mode:[/red] {mode}. Choose from: {', '.join(MODES)}")
        raise typer.Exit(1)

    agent = AgentEngine(max_steps=max_steps, profile=mode)
    label = MODE_LABELS.get(mode, mode)

    console.print(Panel(
        f"[bold]ExperimentPilot CLI[/bold]\n"
        f"Mode: [cyan]{label}[/cyan] | Steps: [cyan]{max_steps}[/cyan]\n"
        f"Type [green]quit[/green] or [green]exit[/green] to leave.",
        border_style="bright_blue",
    ))

    history = []

    while True:
        try:
            task = console.input("\n[bold cyan]Task >[/bold cyan] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not task:
            continue
        if task.lower() in ("quit", "exit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        console.print()
        step_count = 0

        for step_info in agent.run_stream(task, history[-20:]):
            step_count += 1
            print_step(step_info, step_count)

            if step_info["type"] in ("final", "error"):
                break

        console.print(f"[dim]Steps: {step_count}[/dim]")


@app.command()
def run(
    task: str = typer.Argument(..., help="Task to execute"),
    mode: str = typer.Option("general", "-m", "--mode", help=f"Agent mode: {', '.join(MODES)}"),
    max_steps: int = typer.Option(8, "-s", "--steps", help="Max execution steps"),
):
    """Run a single task and exit."""
    agent = AgentEngine(max_steps=max_steps, profile=mode)

    step_count = 0
    for step_info in agent.run_stream(task):
        step_count += 1
        print_step(step_info, step_count)
        if step_info["type"] in ("final", "error"):
            break

    console.print(f"[dim]Steps: {step_count}[/dim]")


@app.command()
def tools():
    """List all available tools."""
    from expilot.tools.registry import TOOLS, TOOL_DESCRIPTIONS
    console.print(Panel("[bold]Available Tools[/bold]", border_style="bright_blue"))
    for name, desc in TOOL_DESCRIPTIONS.items():
        console.print(f"  [cyan]{name}[/cyan] — {desc}")
    console.print(f"\n[dim]Total: {len(TOOLS)} tools[/dim]")


@app.command()
def traces(limit: int = typer.Option(10, "-n", "--limit", help="Number of traces to show")):
    """Show recent tool call traces."""
    from expilot.core.trace import load_traces
    traces_data = load_traces()
    if not traces_data:
        console.print("[dim]No traces recorded yet.[/dim]")
        return

    for tr in traces_data[-limit:][::-1]:
        console.print(Panel(
            f"[bold]{tr['name']}[/bold]\n"
            f"[dim]{tr['timestamp']}[/dim]\n\n"
            f"Input: {str(tr['input'])[:200]}\n"
            f"Output: {tr['output_preview'][:200]}",
            title=f"{tr['step_type']}",
            border_style="dim",
        ))


if __name__ == "__main__":
    app()
