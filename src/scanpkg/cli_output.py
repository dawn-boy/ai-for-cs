from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import networkx as nx

console = Console()

def print_summary(target_pkg, total_deps, total_vulns, critical_paths):
    console.print(Panel(f"[bold blue]Scan Summary for {target_pkg}[/bold blue]", expand=False))
    console.print(f"📦 Total dependencies analyzed: [bold]{total_deps}[/bold]")
    console.print(f"🚨 Vulnerabilities found: [bold red]{total_vulns}[/bold red]")
    console.print(f"⚠️ Critical paths identified: [bold yellow]{critical_paths}[/bold yellow]\n")

def print_vulnerabilities(vulns_dict):
    if not any(vulns_dict.values()):
        console.print("[bold green]✅ No vulnerabilities found![/bold green]\n")
        return

    table = Table(title="Vulnerability Report", show_header=True, header_style="bold magenta")
    table.add_column("Package", style="cyan")
    table.add_column("CVE ID", style="red")
    table.add_column("Severity", justify="center")
    table.add_column("Description")

    for pkg, vulns in vulns_dict.items():
        for v in vulns:
            table.add_row(pkg, v["id"], str(v["severity"]), v["summary"])

    console.print(table)
    console.print()

def print_exploit_paths(G, target_pkg, critical_nodes):
    if not critical_nodes:
        return
        
    console.print("[bold yellow]🧭 Critical Exploit Paths[/bold yellow]")
    
    for node in critical_nodes:
        try:
            paths = list(nx.all_simple_paths(G, source=target_pkg, target=node))
            for path in paths[:3]: # Limit to 3 paths per node
                path_str = " ➔ ".join([f"[cyan]{p}[/cyan]" if p != node else f"[bold red]{p}[/bold red]" for p in path])
                console.print(f"  {path_str}")
        except nx.NetworkXNoPath:
            pass
    console.print()

def print_mitigation(target_pkg, vulns_dict):
    if any(vulns_dict.values()):
        console.print(Panel("[bold green]🛠️ Mitigation Suggestions[/bold green]", expand=False))
        console.print("Recommended upgrade command:")
        
        pkgs_to_upgrade = [pkg for pkg, vulns in vulns_dict.items() if vulns]
        pkg_list = " ".join(pkgs_to_upgrade)
        
        console.print(f"  [bold]sudo apt update && sudo apt upgrade {pkg_list}[/bold]\n")
