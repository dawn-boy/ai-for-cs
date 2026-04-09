import subprocess
import re

def get_package_version(package_name):
    try:
        result = subprocess.run(['dpkg', '-s', package_name], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                return line.split(':', 1)[1].strip()
    except Exception:
        pass
    return "unknown"

def get_dependencies(package_name, depth=1, max_depth=3, visited=None):
    if visited is None:
        visited = set()
        
    if depth > max_depth or package_name in visited:
        return {}
        
    visited.add(package_name)
    deps = []
    
    try:
        result = subprocess.run(['apt-cache', 'depends', package_name], capture_output=True, text=True)
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line.startswith('Depends:'):
                dep_pkg = line.split(':', 1)[1].strip()
                # Remove version constraints like "libc6 (>= 2.14)"
                dep_pkg = re.sub(r'\s*\(.*\)', '', dep_pkg)
                if dep_pkg and dep_pkg not in deps and not dep_pkg.startswith('<'):
                    deps.append(dep_pkg)
    except Exception:
        pass
        
    graph_dict = {package_name: deps}
    for dep in deps:
        graph_dict.update(get_dependencies(dep, depth + 1, max_depth, visited))
        
    return graph_dict
