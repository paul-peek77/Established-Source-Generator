#!/usr/bin/env python3
import os

def main():
    """Generate site map."""

    # Directories to skip entirely (don't even go into them)
    skip_dirs = {'node_modules', '.git', 'venv'}

    # File name patterns to exclude
    exclude_patterns = ['site-map', 'established-source', 'gen-es-deb', 'gen-sm-deb', 'purify-es-deb.py', 'restore-es-uni.py']

    # Groups in the order they should appear
    group_order = [
        '__pycache__',
        'backups',
        'examples',
        'iago_sovereign_memory.egg-info',
        'scripts',
        'tests'
    ]

    # Collect all files
    files = []
    for root, dirs, filenames in os.walk('.'):
        # Skip unwanted directories
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for fname in filenames:
            # Skip excluded patterns
            if any(p in fname for p in exclude_patterns):
                continue

            # Create full path
            path = os.path.join(root, fname)
            if not path.startswith('./'):
                path = './' + path.lstrip('./')
            files.append(path)

    # Sort case-insensitively
    files.sort(key=str.lower)

    # Categorize
    groups = {g: [] for g in group_order}
    other_dirs = []
    root_files = []

    for f in files:
        parts = f.split('/')
        if len(parts) == 2:  # Root file (./file.txt)
            root_files.append(f)
        else:
            dir_name = parts[1]  # Directory after ./
            if dir_name in group_order:
                groups[dir_name].append(f)
            else:
                other_dirs.append(f)

    # Write output
    with open('site-map.txt', 'w') as out:
        count = 1

        # Write files in specific directories (in order)
        for dir_name in group_order:
            for f in sorted(groups[dir_name], key=str.lower):
                out.write(f"{count:03d} {f}\n")
                count += 1

        # Write other directories
        for f in sorted(other_dirs, key=str.lower):
            out.write(f"{count:03d} {f}\n")
            count += 1

        # Write root files
        for f in sorted(root_files, key=str.lower):
            out.write(f"{count:03d} {f}\n")
            count += 1

    print(f"✓ Generated site-map.txt with {count-1} files")

if __name__ == '__main__':
    main()
