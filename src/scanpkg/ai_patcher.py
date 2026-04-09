import os
import requests
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown

console = Console()

def generate_patch(package_name, cve_id, description):
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        console.print("[yellow]⚠️ GROQ_API_KEY environment variable not found. Skipping AI patch generation.[/yellow]")
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

    # Using Groq API (OpenAI compatible endpoint) with Llama 3
    url = "https://api.groq.com/openai/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": "You are a helpful cybersecurity expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.2
    }
    
    try:
        with console.status(f"[bold cyan]🤖 AI is analyzing {cve_id} and generating a patch via Groq...[/bold cyan]"):
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            text_response = data["choices"][0]["message"]["content"]
            
            console.print(Panel(
                Markdown(text_response), 
                title=f"[bold cyan]🧠 AI Patch Proposal: {package_name} ({cve_id})[/bold cyan]", 
                border_style="cyan",
                expand=False
            ))
            console.print()
            
    except Exception as e:
        console.print(f"[red]Failed to generate AI patch for {cve_id}: {e}[/red]")
