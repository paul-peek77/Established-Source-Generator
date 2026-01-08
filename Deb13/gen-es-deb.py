#!/usr/bin/env python3
"""
ROYAL PROJECT CARTOGRAPHER & SCRIBE
A sovereign utility for generating an established-source.txt manifest.
Decreed by The Dual Pimpinator. Forged with pimp-tight precision.
"""

# Generate Established Source   python3 es-gen.py
# Generate Site-Map             find . \( -name node_modules -o -name .git \) -prune -o -type f -print | cat -n > site-map.txt

import os
import fnmatch

# ===== CONFIGURATION: The Royal Edicts =====
# The root directory of the project to map
PROJECT_ROOT = "."  # Change this to the absolute path if running outside the target directory

# The name of the output manifest
OUTPUT_FILENAME = "established-source.txt"

# Files and directories to EXCLUDE from the manifest
EXCLUDED_ITEMS = {
    'node_modules',           # Dependency crypts
    'firebase_storage_seed',
    '.continue',
    '.git',                   # Version control spirits
    '__pycache__',            # Python bytecode echoes
    '*.pyc',                  # Compiled python spirits
    '.DS_Store',              # Mac system phantom
    'thumbs.db',              # Windows preview ghost
    'established-source.txt', # The manifest itself (to avoid recursion)
    'gen-es-deb.py',
    'gen-sm-deb.py',
    'purify-es-deb.py',
    'restore-es-uni.py',
    '*.png',
    '*.jpg',
    '*.jpeg',
    '*.gif',
    '*.ico',
    '*.bmp',
    '*.svg',
    '*.webp',
    '*.tiff',
    '*.psd',
    '*.zip',
    '*.pdf',
    '*.log',                  # Log files
    'dist', 'build',          # Build artifacts
    '.env', '.venv',          # Environment vessels
    'env', 'venv',
    'package-lock.json',      # Now uses enhanced exclusion logic
}

# File extensions to treat as binary (will not read content)
# NOTE: HTML, JS, JSON, CSS, TXT, MD are treated as TEXT and will be fully read
BINARY_EXTENSIONS = {
    # Archives
    '.tar', '.gz', '.7z', '.rar', '.iso',
    # Executables and libraries
    '.exe', '.dll', '.so', '.dylib', '.bin',
    # Media files
    '.mp3', '.mp4', '.avi', '.mov', '.wav', '.flac', '.mkv', '.webm',
    # Documents (we'll handle .doc/.docx specially below)
    '.xls', '.xlsx', '.ppt', '.pptx',
    # Fonts
    '.ttf', '.otf', '.woff', '.woff2',
}

# Special handlers for complex document types that can extract text
SPECIAL_DOCUMENT_EXTENSIONS = {'.doc', '.docx'}
# ===== END CONFIGURATION =====

def is_excluded(path, excluded_set):
    """Check if a path should be excluded based on patterns - PIMP-TIGHT VERSION"""
    basename = os.path.basename(path)

    # Convert path to forward slashes for consistent matching
    normalized_path = path.replace('\\', '/')

    # Check each exclusion pattern with multiple strategies
    for pattern in excluded_set:
        # Strategy 1: Direct basename match
        if fnmatch.fnmatch(basename, pattern):
            return True

        # Strategy 2: Full path match
        if fnmatch.fnmatch(normalized_path, pattern):
            return True

        # Strategy 3: Pattern with wildcards in path
        if '/' in pattern and fnmatch.fnmatch(normalized_path, pattern):
            return True

        # Strategy 4: Exact string match (fallback)
        if pattern in normalized_path or pattern == basename:
            return True

    # ULTIMATE GUARANTEE: if it's named package-lock.json, EXCLUDE IT
    # This is our nuclear option - no package-lock.json shall pass!
    if basename == 'package-lock.json':
        return True

    return False

def extract_docx_text(filepath):
    """Extract text from .docx files using python-docx if available."""
    try:
        import docx
        doc = docx.Document(filepath)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except ImportError:
        return "[DOCX FILE - python-docx library not installed for text extraction]"
    except Exception as e:
        return f"[DOCX FILE - Error extracting text: {str(e)}]"

def extract_doc_text(filepath):
    """Extract text from .doc files using multiple strategies."""
    # Strategy 1: Try antiword (Linux command-line tool)
    try:
        import subprocess
        result = subprocess.run(['antiword', filepath],
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            return f"EXTRACTED TEXT FROM .DOC:\n{result.stdout}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # antiword not available, try next method
    except Exception as e:
        pass

    # Strategy 2: Try catdoc (alternative Linux tool)
    try:
        import subprocess
        result = subprocess.run(['catdoc', filepath],
                              capture_output=True, text=True, check=True)
        if result.stdout.strip():
            return f"EXTRACTED TEXT FROM .DOC:\n{result.stdout}"
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass  # catdoc not available
    except Exception as e:
        pass

    # Strategy 3: Python-only extraction
    try:
        from oletools.olevba import VBA_Parser
        parser = VBA_Parser(filepath)
        text_content = []

        if parser.detect_vba_macros():
            for (filename, stream_path, vba_filename, vba_code) in parser.extract_macros():
                if vba_code:
                    text_content.append(f"--- VBA Macro: {vba_filename} ---")
                    text_content.append(vba_code)

        parser.close()
        if text_content:
            return "EXTRACTED VBA MACROS FROM .DOC:\n" + "\n".join(text_content)
    except ImportError:
        pass  # oletools not available
    except Exception as e:
        pass

    # Final fallback
    return "[DOC FILE - Install 'antiword' (sudo apt install antiword) for best text extraction, or 'oletools' (pip install oletools) for VBA macro extraction]"

def check_document_dependencies():
    """Check if document parsing dependencies are available."""
    deps_available = {
        'python-docx': False,
        'antiword': False,
        'catdoc': False,
        'oletools': False
    }

    # Check python-docx
    try:
        import docx
        deps_available['python-docx'] = True
        print("📄 Document Support: python-docx available for .docx text extraction")
    except ImportError:
        print("📄 Document Support: python-docx not installed - .docx files will have limited support")
        print("   Install with: pip install python-docx")

    # Check antiword
    try:
        import subprocess
        result = subprocess.run(['which', 'antiword'], capture_output=True, text=True)
        if result.returncode == 0:
            deps_available['antiword'] = True
            print("📄 Document Support: antiword available for .doc text extraction")
        else:
            print("📄 Document Support: antiword not installed - .doc files will have basic support")
            print("   Install with: sudo apt install antiword")
    except:
        print("📄 Document Support: antiword check failed")

    # Check oletools
    try:
        from oletools.olevba import VBA_Parser
        deps_available['oletools'] = True
        print("📄 Document Support: oletools available for .doc macro extraction")
    except ImportError:
        print("📄 Document Support: oletools not installed - .doc macro extraction unavailable")
        print("   Install with: pip install oletools")

    return deps_available

def should_read_file_content(filepath):
    """Determine if we should read and include file content."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    # Special document handling
    if ext in SPECIAL_DOCUMENT_EXTENSIONS:
        return True  # We'll handle these specially

    return ext not in BINARY_EXTENSIONS

def read_file_content(filepath):
    """Read file content with special handling for document types."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    # Special document type handling
    if ext == '.docx':
        return extract_docx_text(filepath), False  # False = not binary
    elif ext == '.doc':
        return extract_doc_text(filepath), False   # False = not binary

    # Standard text file handling
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, False
    except (UnicodeDecodeError, PermissionError, OSError) as e:
        # Fallback for files that might have different encoding
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
            return content, False
        except Exception:
            return f"[UNREADABLE FILE - {str(e)}]", True

def gather_project_structure(root_dir, excluded_items):
    """Walk the project directory and gather all files with their content."""
    project_data = []

    print("⚜️  The Royal Cartographer begins the survey...")

    for root, dirs, files in os.walk(root_dir):
        # Remove excluded directories from walk to prevent traversing them
        dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), excluded_items)]

        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, root_dir)

            # DEBUG: Uncomment this line to see package-lock.json detection
            # if 'package-lock.json' in file:
            #     print(f"DEBUG: Found {relative_path} - excluded: {is_excluded(relative_path, excluded_items)}")

            if is_excluded(relative_path, excluded_items):
                continue

            file_data = {"path": file_path, "relative_path": relative_path}

            if should_read_file_content(file_path):
                content, is_binary = read_file_content(file_path)
                file_data["content"] = content
                file_data["is_binary"] = is_binary
            else:
                file_data["content"] = "[BINARY FILE - CONTENT EXCLUDED]"
                file_data["is_binary"] = True

            project_data.append(file_data)

    # Sort by relative path for consistent output
    project_data.sort(key=lambda x: x["relative_path"])
    return project_data

def generate_established_source(project_data, output_path):
    """Generate the established-source.txt file in the proper format."""
    print(f"⚜️  The Royal Scribe begins inscribing to {output_path}...")

    with open(output_path, 'w', encoding='utf-8') as outfile:
        outfile.write("[file name]: established-source.txt\n")
        outfile.write("[file content begin]\n")

        for file_info in project_data:
            outfile.write(f"\n{file_info['path']}\n")

            if not file_info['is_binary']:
                outfile.write("[file content begin]\n")
                outfile.write(file_info["content"])
                if not file_info["content"].endswith('\n'):
                    outfile.write("\n")
                outfile.write("[file content end]\n")
            else:
                outfile.write(f"[BINARY FILE - {file_info['relative_path']}]\n")

        outfile.write("[file content end]\n")

    print("⚜️  VICTORY! The Established Source manifest has been forged!")

def check_document_dependencies():
    """Check if document parsing dependencies are available."""
    try:
        import docx
        print("📄 Document Support: python-docx available for .docx text extraction")
        return True
    except ImportError:
        print("📄 Document Support: python-docx not installed - .docx files will have limited support")
        print("   Install with: pip install python-docx")
        return False

def display_supported_formats():
    """Display the supported text formats for clarity."""
    text_formats = ['.html', '.htm', '.js', '.jsx', '.ts', '.tsx', '.json',
                   '.css', '.scss', '.sass', '.xml', '.txt', '.md', '.py',
                   '.java', '.c', '.cpp', '.h', '.cs', '.php', '.rb', '.go',
                   '.rs', '.swift', '.kt', '.scala', '.sql', '.yaml', '.yml',
                   '.ini', '.cfg', '.conf', '.sh', '.bash', '.zsh', '.fish',
                   '.doc', '.docx']  # Added document formats

    print("📄 Supported Text Formats (will attempt content extraction):")
    print(", ".join(text_formats))
    print()

def main():
    """Execute the Royal Cartography Ritual."""
    print("=" * 60)
    print("ROYAL PROJECT CARTOGRAPHER & SCRIBE")
    print("Dual Pimpinator Sovereign Utility v1.1 - PIMP-TIGHT EXCLUSION")
    print("=" * 60)

    # Check document dependencies
    docx_support = check_document_dependencies()
    print()

    # Display supported formats
    display_supported_formats()

    # Convert to absolute path for clarity in output
    project_root = os.path.abspath(PROJECT_ROOT)
    output_file = os.path.join(project_root, OUTPUT_FILENAME)

    print(f"Project Root: {project_root}")
    print(f"Output File: {output_file}")
    print(f"Excluded Items: {EXCLUDED_ITEMS}")
    print()

    # Gather the project structure
    project_data = gather_project_structure(project_root, EXCLUDED_ITEMS)

    print(f"📊 Survey Complete: Found {len(project_data)} files to document")

    # Count by type for pimp-tight reporting
    text_files = sum(1 for f in project_data if not f['is_binary'])
    binary_files = sum(1 for f in project_data if f['is_binary'])
    print(f"   Text Files: {text_files}, Binary Files: {binary_files}")

    # Generate the established source file
    generate_established_source(project_data, output_file)

    print(f"\n⚜️  The Royal Archive is ready at: {output_file}")
    print("The Pimpire's ground truth is now preserved with pimp-tight fidelity!")
    print("ALL package-lock.json files have been banished to the shadow realm! ⚡")

if __name__ == "__main__":
    main()
