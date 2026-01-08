# [file name]: gen-es.py
# [directory]: ./ (Run in the project root)
import os
import fnmatch

# ===== CONFIGURATION: The Royal Edicts =====
OUTPUT_FILENAME = "established-source.txt"
PROJECT_ROOT = "."

EXCLUDED_ITEMS = {
    'node_modules', '.git', '__pycache__', '*.pyc', '.DS_Store', 
    'thumbs.db', 'package-lock.json', 'venv', '.venv', 'env',
    '.env', '*.log', 'dist', 'build', '.continue', 'data', '*.png',
    '*.jpg', '*.jpeg', '*.gif', '*.ico', '*.svg', 'gen-es.py',
    'gen-sm.py', 'established-source.txt', 'site-map.txt',
}

WHITELISTED_FILES = {
    'package.json', 'requirements.txt', 'tsconfig.json', 
    'vite.config.ts', 'firebase.json'
}

def is_excluded(path, excluded_set):
    basename = os.path.basename(path)
    if basename in WHITELISTED_FILES:
        return False
    normalized_path = path.replace('\\', '/')
    for pattern in excluded_set:
        if fnmatch.fnmatch(basename, pattern) or fnmatch.fnmatch(normalized_path, pattern):
            return True
    return False

def main():
    current_dir = os.path.basename(os.getcwd())
    print(f"⚜️ Mapping territory with Relative Sovereignty: {current_dir}")
    project_data = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Prevent traversing into excluded dependency crypts
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), EXCLUDED_ITEMS)]
        
        for file in files:
            file_path = os.path.join(root, file)
            # FORCE RELATIVE PATH: Establishing the root as "."
            rel_path = os.path.relpath(file_path, PROJECT_ROOT)
            if not rel_path.startswith('.'):
                rel_path = os.path.join(".", rel_path)
            
            if is_excluded(rel_path, EXCLUDED_ITEMS):
                continue
            
            try:
                # Using 'replace' errors to handle any weird Windows encoding snooganly
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                project_data.append({
                    "rel_path": rel_path, 
                    "content": content
                })
            except Exception as e:
                print(f"⚠️ Skipping {file}: {e}")
                continue

    project_data.sort(key=lambda x: x["rel_path"])
    
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        f.write(f"[source territory]: {current_dir}\n")
        f.write(f"[file name]: {OUTPUT_FILENAME}\n")
        f.write("[file content begin]\n")
        for info in project_data:
            # We record only the relative path (e.g., .\README.md)
            f.write(f"\n{info['rel_path']}\n")
            f.write("[file content begin]\n")
            f.write(info['content'])
            if not info['content'].endswith('\n'): f.write('\n')
            f.write("[file content end]\n")
        f.write("[file content end]\n")
    print(f"⚜️ VICTORY! Standardized Relative ES forged: {OUTPUT_FILENAME}")

if __name__ == "__main__":
    main()