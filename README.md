# ScanPkg - AI-Powered Cybersecurity CLI

An AI-powered cybersecurity CLI tool that detects **reachable vulnerabilities in installed Linux packages** and provides **automated mitigation suggestions**.

It goes beyond traditional vulnerability scanners by analyzing **dependency graphs** and identifying which vulnerabilities are actually exploitable in the current system context using a Graph Neural Network (GNN).

## Features

- **Dependency Graph Extraction**: Extracts dependency information using `apt-cache`.
- **Graph Feature Engineering**: Converts nodes into feature vectors (depth, degree, vulnerability prior).
- **Graph Neural Network (GNN)**: Uses PyTorch Geometric to classify nodes (safe, vulnerable, critical).
- **External Vulnerability Lookup**: Queries the Open Source Vulnerabilities (OSV) API.
- **Risk Analysis**: Combines GNN predictions and API results to determine reachability.
- **CLI-Based Output**: Clean, structured, and readable terminal output using `rich`.

## Setup

1. Ensure you have Python 3 installed.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool by passing the name of an installed package:

```bash
python src/scanpkg/main.py <package_name>
```

Example:

```bash
python src/scanpkg/main.py curl
```

You can also specify the dependency resolution depth (default is 2):

```bash
python src/scanpkg/main.py curl --depth 3
```

## Output

The tool provides a structured report including:
- **Scan Summary**: Target package, total dependencies, vulnerabilities found, critical paths.
- **Vulnerability Report**: CVE ID, severity, and description for each vulnerability.
- **Exploit Path**: Clear dependency chain (e.g., App → A → B → Vulnerable Package).
- **Mitigation Suggestions**: Recommended upgrade commands.
