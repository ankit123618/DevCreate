import os

def detect_project():
    if os.path.exists("package.json"):
        return "node"
    elif os.path.exists("requirements.txt"):
        return "python"
    elif os.path.exists("composer.json"):
        return "php"
    elif os.path.exists("go.mod"):
        return "go"
    return None
