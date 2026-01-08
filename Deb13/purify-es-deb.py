# [file name]: purify-es-deb.py
# [directory]: ./ (Project Root)
import os

def purify_relative_manifest(filename="established-source.txt"):
    print(f"⚜️ Initiating Relative Alchemical Purification on {filename}...")

    if not os.path.exists(filename):
        print(f"❌ Error: {filename} not found! The Scroll is missing.")
        return

    with open(filename, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    # --- RITUAL 1: Apostrophe & Slash Exorcism ---
    print("🪄 Exorcising traitorous slashes from JavaScript strings...")
    content = content.replace("/'s", "'s")

    # --- RITUAL 2: JSON Comma Restoration ---
    print("🪄 Sanitizing package.json syntax for the OS Guardian...")
    old_json_line = '"dev:all": "concurrently \\"npm run dev\\" \\"npm run dev:backend\\""'
    new_json_line = '"dev:all": "concurrently \\"npm run dev\\" \\"npm run dev:backend\\","'

    if old_json_line in content and f"{old_json_line}," not in content:
        content = content.replace(old_json_line, new_json_line)

    # --- RITUAL 3: Path Consistency (Linux version) ---
    # On Linux, ensure consistent forward slashes
    print("🪄 Harmonizing path separators for Linux...")
    # Convert any Windows backslashes to forward slashes
    content = content.replace('\\.\\', './')
    content = content.replace('\\./', './')

    # Ensure consistent ./ prefix
    import re
    content = re.sub(r'(\n)\.\\', r'\1./', content)

    output_name = f"PURIFIED-{filename}"
    with open(output_name, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"⚜️ VICTORY! Purified Relative Manifest forged: {output_name}")
    print("The Pimpire's ground truth is now purified and Linux-ready.")

if __name__ == "__main__":
    purify_relative_manifest()
