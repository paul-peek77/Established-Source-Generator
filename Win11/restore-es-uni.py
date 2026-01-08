# [file name]: restore-es.py
# [directory]: ./ (Run in the folder where you want to restore)
import os

def restore_pimpire_standard():
    # Priority: Check for Purified version first
    es_filename = "PURIFIED-established-source.txt" if os.path.exists("PURIFIED-established-source.txt") else "established-source.txt"
    
    print(f"⚜️ Shadow Scribe restoring from: {es_filename}")
    
    if not os.path.exists(es_filename):
        print("❌ Error: Manifest not found!")
        return

    with open(es_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    collecting = False
    file_content = []
    restored_count = 0
    current_file_path = None

    for line in lines:
        # Detect the Relative Path marker (.\README.md, etc.)
        if not collecting and (line.strip().startswith(".\\") or line.strip().startswith("./")):
            current_file_path = line.strip()
            continue

        if "[file content begin]" in line:
            if not collecting and restored_count > 0:
                collecting = True
                file_content = []
                continue
            elif restored_count == 0:
                # Skip the ES header line
                restored_count += 1
                continue

        if "[file content end]" in line and collecting:
            if current_file_path:
                # Recreate subdirectories if they exist in the path
                os.makedirs(os.path.dirname(current_file_path), exist_ok=True)
                with open(current_file_path, 'w', encoding='utf-8') as f_out:
                    f_out.writelines(file_content)
                print(f"✅ Restored: {current_file_path}")
                restored_count += 1
            collecting = False
            continue

        if collecting:
            file_content.append(line)

    print(f"\n⚜️ VICTORY! {restored_count - 1} artifacts resurrected.")

if __name__ == "__main__":
    restore_pimpire_standard()