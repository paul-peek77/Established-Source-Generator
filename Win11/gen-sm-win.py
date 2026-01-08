# [file name]: gen-sm.py
# [directory]: C:\Users\krist\agent\scripts\
# [file content begin]
import os

def generate_site_map():
    PROJECT_ROOT = "."
    OUTPUT_FILENAME = "site-map.txt"
    EXCLUDED_DIRS = {'.git', 'node_modules', '__pycache__'}
    
    print("⚜️ Mapping the territory...")
    entries = []
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Identify node_modules but don't go inside
        for d in list(dirs):
            if d in EXCLUDED_DIRS:
                rel_dir = os.path.join(root, d).replace('\\', '/')
                entries.append(f"{rel_dir} # Excluded Directory")
                dirs.remove(d) # Don't recurse

        for file in files:
            rel_path = os.path.join(root, file).replace('\\', '/')
            if not rel_path.startswith('./'):
                rel_path = './' + rel_path
            entries.append(rel_path)

    entries.sort()
    
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        for i, entry in enumerate(entries, 1):
            f.write(f"{i:03} {entry}\n")
            
    print(f"⚜️ Site map forged at {OUTPUT_FILENAME}")

if __name__ == "__main__":
    generate_site_map()
# [file content end]