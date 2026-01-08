# [file name]: purify-es.py
# [directory]: ./ (Project Root)
import os
import re

def purify_relative_manifest(filename="established-source.txt"):
    print(f"⚜️ Initiating Relative Alchemical Purification on {filename}...")
    
    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found! The Scroll is missing.")
        return

    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # --- RITUAL 1: Apostrophe & Slash Exorcism ---
    # Fix the "Diamond/'s" and "Sterling/'s" issues that caused the SyntaxError
    print("🪄 Exorcising traitorous slashes from JavaScript strings...")
    # Globally replaces the incorrect forward-slash escape with the clean version
    content = content.replace("/'s", "'s") 
    
    # --- RITUAL 2: JSON Comma Restoration ---
    # Fix the specific EJSONPARSE error in the package.json scripts
    print("🪄 Sanitizing package.json syntax for the OS Guardian...")
    # This targets the exact missing comma line we identified in the Diamondz project
    old_json_line = '"dev:all": "concurrently \\"npm run dev\\" \\"npm run dev:backend\\""'
    new_json_line = '"dev:all": "concurrently \\"npm run dev\\" \\"npm run dev:backend\\","'
    
    if old_json_line in content and f"{old_json_line}," not in content:
        content = content.replace(old_json_line, new_json_line)

    # --- RITUAL 3: Path Consistency ---
    # Ensures all paths use the Windows-standard backslash for relative sovereignty
    print("🪄 Harmonizing path separators...")
    # Find path markers and ensure they use backslashes after the initial dot
    content = re.sub(r'(\n\.)/([^\n]+)', r'\1\\\2', content)

    output_name = f"PURIFIED-{filename}"
    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"⚜️ VICTORY! Purified Relative Manifest forged: {output_name}")
    print("The Pimpire's ground truth is now purified and path-agnostic.")

if __name__ == "__main__":
    purify_relative_manifest()