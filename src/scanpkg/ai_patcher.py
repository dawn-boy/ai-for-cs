import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def generate_patch(package_name, cve_id, description):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        console.print("[yellow]⚠️ GEMINI_API_KEY environment variable not found. Skipping AI patch generation.[/yellow]")
        return

    prompt = f"""
    You are an expert cybersecurity researcher and Linux system administrator. 
    A vulnerability has been detected in a Linux package.
    
    Package: {package_name}
    Vulnerability ID: {cve_id}
    Description: {description}
    
    Please provide:
    1. **Root Cause Analysis**: A brief explanation of how the vulnerability works.
    2. **Conceptual Patch**: A code snippet showing how the vulnerable code is typically patched (if applicable).
    3. **Workaround / Fix Script**: A bash script or configuration command to mitigate the issue immediately without waiting for an upstream patch.
    
    Format your response in clean Markdown. Keep it concise, actionable, and focused on remediation.
    """

    # Using Gemini 2.5 Flash for fast, accurate reasoning
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2
        }
    }
    
    try:
        with console.status(f"[bold cyan]🤖 AI is analyzing {cve_id} and generating a patch...[/bold cyan]"):
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
            
            text_response = data["candidates"][0]["content"]["parts"][0]["text"]
            
            console.print(Panel(
                Markdown(text_response), 
                title=f"[bold cyan]🧠 AI Patch Proposal: {package_name} ({cve_id})[/bold cyan]", 
                border_style="cyan",
                expand=False
            ))
            console.print()
            
    except Exception as e:
        console.print(f"[red]Failed to generate AI patch for {cve_id}: {e}[/red]")
