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
    elif any(f.endswith(".c") for f in os.listdir(".")):
        return "c"
    elif any(f.endswith(".cpp") for f in os.listdir(".")):
        return "cpp"
    elif os.path.exists("pom.xml") or any(f.endswith(".java") for f in os.listdir(".")):
        return "java"
    return None
