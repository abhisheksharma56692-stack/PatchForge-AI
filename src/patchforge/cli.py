"""PatchForge AI CLI powered by Typer and Rich."""
import os
import sys
from typing import Optional

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

app = typer.Typer(
    name="patchforge",
    help="[🎃] PatchForge AI — Unified Autonomous Vulnerability Remediation Engine",
    add_completion=False,
)
console = Console(legacy_windows=False)


@app.command()
def run(
    sarif: str = typer.Option(..., "--sarif", "-s", help="Path to SARIF diagnostic report"),
    repo_path: str = typer.Option(".", "--repo-path", "-r", help="Path to target source repository"),
    language: str = typer.Option("python", "--language", "-l", help="Repository language (python, javascript, go)"),
    max_iterations: int = typer.Option(5, "--max-iterations", "-k", help="Max bounded self-healing iterations"),
    aws_region: str = typer.Option("us-east-1", "--aws-region", help="AWS Region for Bedrock, S3, DynamoDB"),
    auto_pr: bool = typer.Option(False, "--auto-pr", help="Automatically dispatch Pull Request on verification"),
    use_stubs: bool = typer.Option(False, "--use-stubs", help="Use stubbed analysis modules for testing"),
):
    """Executes the autonomous vulnerability remediation pipeline."""
    console.print(
        Panel.fit(
            "[bold orange1]🎃 PatchForge AI — Autonomous Remediation Pipeline[/bold orange1]\n"
            f"[dim]SARIF Report:[/dim] {sarif} | [dim]Language:[/dim] {language} | [dim]AWS Region:[/dim] {aws_region}",
            border_style="orange1",
        )
    )

    if not os.path.exists(sarif):
        console.print(f"[bold red]❌ Error:[/bold red] SARIF file not found: {sarif}")
        raise typer.Exit(code=1)

    os.environ["PATCHFORGE_USE_STUBS"] = "true" if use_stubs else "false"

    try:
        from patchforge.orchestrator.graph import build_remediation_graph
        graph = build_remediation_graph()
        initial_state = {
            "sarif_raw": {"file_path": sarif},
            "vulnerability": None,
            "cwe_id": "CWE-UNKNOWN",
            "cve_id": None,
            "ast_slice": None,
            "formal_invariants": None,
            "reproduction_test": None,
            "candidate_patch_diff": None,
            "iteration_count": 0,
            "max_iterations": max_iterations,
            "error_feedback_history": [],
            "sandbox_result": None,
            "audit_passed": False,
            "pr_url": None,
            "status": "AWAKENING",
        }
        console.print("[green]✓[/green] State graph initialized. Commencing remediation loop...")
        final_state = graph.invoke(initial_state)
        
        status = final_state.get("status", "UNKNOWN")
        if status == "TOMBSTONE_READY" or final_state.get("pr_url"):
            console.print(Panel(f"🎉 Remediation Succeeded!\nPR URL: {final_state.get('pr_url')}", style="bold green"))
        else:
            console.print(Panel(f"⚠️ Remediation completed with status: {status}", style="bold yellow"))
            
    except Exception as e:
        console.print(f"[bold red]❌ Execution failed:[/bold red] {e}")
        raise typer.Exit(code=1)


@app.command()
def status():
    """Checks operational status of Docker sandbox, AWS credentials, and LLM APIs."""
    console.print(Panel.fit("[bold purple]🦇 PatchForge AI — Health & Service Telemetry[/bold purple]", border_style="purple"))

    table = Table(title="System Diagnostics", border_style="dim")
    table.add_column("Subsystem", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Details")

    # Python version
    table.add_row("Python Runtime", "[green]ONLINE[/green]", f"{sys.version.split()[0]}")

    # Check Docker
    try:
        import docker
        client = docker.from_env()
        client.ping()
        table.add_row("Docker Engine", "[green]CONNECTED[/green]", "Hermetic micro-sandbox ready")
    except Exception as ex:
        table.add_row("Docker Engine", "[yellow]STANDALONE[/yellow]", f"Daemon inactive ({str(ex)[:35]}...)")

    # Check AWS credentials
    try:
        import boto3
        session = boto3.Session()
        creds = session.get_credentials()
        if creds:
            table.add_row("AWS Credentials", "[green]CONFIGURED[/green]", f"Key ID: {creds.access_key[:4]}****")
        else:
            table.add_row("AWS Credentials", "[yellow]MOCK/DEV[/yellow]", "No active AWS session (Moto active)")
    except Exception:
        table.add_row("AWS Credentials", "[yellow]MOCK/DEV[/yellow]", "Using local in-memory mocks")

    console.print(table)


@app.command()
def dashboard(
    host: str = typer.Option("0.0.0.0", "--host", "-h", help="Bind host for FastAPI backend"),
    port: int = typer.Option(8000, "--port", "-p", help="Port for FastAPI backend"),
    reload: bool = typer.Option(False, "--reload", help="Enable hot reload"),
):
    """Launches the 🎃 Halloween Operations Dashboard API backend."""
    import uvicorn
    console.print(Panel.fit(
        f"[bold orange1]🎃 Launching Halloween Dashboard Backend[/bold orange1]\n"
        f"API URL: [cyan]http://{host}:{port}[/cyan]\n"
        f"WebSocket: [cyan]ws://{host}:{port}/ws/pipeline[/cyan]",
        border_style="orange1"
    ))
    uvicorn.run("patchforge.api.server:app", host=host, port=port, reload=reload)


if __name__ == "__main__":
    app()
