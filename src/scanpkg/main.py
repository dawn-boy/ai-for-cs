import argparse
import sys
from rich.console import Console

from extractor import get_dependencies, get_package_version
from vulnerability import check_vulnerabilities
from graph_builder import build_networkx_graph, extract_features
from gnn_model import train_synthetic_model, predict_risk
from cli_output import print_summary, print_vulnerabilities, print_exploit_paths, print_mitigation

console = Console()

def main():
    parser = argparse.ArgumentParser(description="AI-powered cybersecurity CLI tool for Linux packages.")
    parser.add_argument("package", help="The target package to scan")
    parser.add_argument("--depth", type=int, default=2, help="Dependency resolution depth")
    
    args = parser.parse_args()
    target_pkg = args.package
    
    with console.status(f"[bold green]Analyzing {target_pkg} dependencies...[/bold green]"):
        dep_dict = get_dependencies(target_pkg, max_depth=args.depth)
        
    if not dep_dict:
        console.print(f"[bold red]Error:[/bold red] Could not resolve dependencies for {target_pkg}. Is it installed?")
        sys.exit(1)
        
    G = build_networkx_graph(dep_dict)
    
    vulns_dict = {}
    with console.status("[bold green]Checking OSV for vulnerabilities...[/bold green]"):
        for node in G.nodes():
            version = get_package_version(node)
            vulns = check_vulnerabilities(node, version)
            if vulns:
                vulns_dict[node] = vulns
                
    with console.status("[bold green]Running GNN Risk Analysis...[/bold green]"):
        data, node_mapping = extract_features(G, vulns_dict)
        model = train_synthetic_model()
        preds, probs = predict_risk(model, data)
        
    reverse_mapping = {v: k for k, v in node_mapping.items()}
    critical_nodes = []
    
    for i, pred in enumerate(preds):
        if pred.item() == 2 or len(vulns_dict.get(reverse_mapping[i], [])) > 0:
            critical_nodes.append(reverse_mapping[i])
            
    total_vulns = sum(len(v) for v in vulns_dict.values())
    
    # Output Report
    console.print("\n")
    print_summary(target_pkg, len(G.nodes()), total_vulns, len(critical_nodes))
    print_vulnerabilities(vulns_dict)
    print_exploit_paths(G, target_pkg, critical_nodes)
    print_mitigation(target_pkg, vulns_dict)

if __name__ == "__main__":
    main()
