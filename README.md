## The Established Source System

#### A cross‑platform utility for generating a complete, text‑based manifest of a project directory. The manifest captures file paths, readable content, and structural information in a standardized format suitable for archival, analysis, and reconstruction.

---

*This project is provided for portfolio review only. No permission is granted for reuse, modification, or redistribution.*

---

#### Overview

The system includes:

- Debian version with advanced document extraction
- Windows version with relative‑path normalization
- Purification tools for correcting path inconsistencies
- Platform‑specific restoration tools
- Site‑map generators for quick directory indexing

This project demonstrates:

- filesystem traversal
- exclusion logic
- document parsing
- reversible manifest workflows
- cross‑platform scripting
- deterministic reconstruction

---

#### Components

The Established Source System consists of four primary tools, each implemented for both Debian and Windows environments.

1. Manifest Generator (gen-es-*.py)

Creates established-source.txt by:

- walking the project directory
- excluding dependency folders and binary formats
- reading text files in full
- extracting content from .doc and .docx when possible
- marking binary files with placeholders
- producing a stable, sorted manifest

The Debian version includes optional support for:

- python-docx
- antiword
- catdoc
- oletools

The Windows version focuses on consistent relative paths and UTF‑8 handling.

---

2. Site‑Map Generator (gen-sm-*.py)

Produces a simple, ordered site-map.txt listing all files in the project.

Useful for:

- quick indexing
- debugging exclusion rules
- verifying directory structure

---

3. Purifier (purify-es-*.py)

Cleans and normalizes an existing manifest.

The purifier:

- fixes path inconsistencies
- corrects known JSON formatting issues
- harmonizes separators for the target OS
- removes problematic escape sequences

This ensures the manifest is safe for restoration on the intended platform.

---

4. Restorers (restore-es-*.py)

The restoration process is platform‑specific.

Each OS has its own restorer:

- Debian/Linux: restore-es-deb.py
- Windows: restore-es-win.py

Both restorers:

- read the manifest line‑by‑line
- detect file boundaries
- recreate directories
- write file contents exactly as recorded
- skip binary placeholders
- restore only text‑based artifacts

This ensures correct path handling and consistent reconstruction on each platform.

---

#### Usage

Generate a Manifest

Debian/Linux
`
python3 gen-es-deb.py
`

Windows
`
python gen-es-win.py
`

This produces:

`
established-source.txt
`

---

Generate a Site Map

Debian/Linux
`
python3 gen-sm-deb.py
`

Windows
`
python gen-sm-win.py
`

---

Purify a Manifest

Debian/Linux
`
python3 purify-es-deb.py
`

Windows
`
python purify-es-win.py
`

This produces:

`
PURIFIED-established-source.txt
`

---

Restore a Project

Place the manifest in an empty directory and run the appropriate restorer.

Debian/Linux
`
python3 restore-es-deb.py
`

Windows
`
python restore-es-win.py
`

Both scripts will:

- recreate directories
- restore all text files
- report each restored artifact

---

#### Design Philosophy

The Established Source System is built around three principles:

1. Deterministic Output

The manifest is sorted, stable, and predictable.
Running the generator twice on the same project yields identical results.

2. Text‑First Approach

Readable content is preserved.
Binary files are acknowledged but not embedded.

3. Cross‑Platform Consistency

Both OS versions follow the same conceptual workflow while respecting platform differences:

- path separators
- encoding behavior
- available document‑extraction tools

---

#### Limitations

- Binary files are not restored (placeholders only).
- .doc and .docx extraction depends on optional tools.
- File permissions are not preserved.
- Extremely large projects may produce very large manifests.

---

#### Purpose

This system was created to support:

- AI‑assisted debugging
- long‑form project ingestion
- deterministic reconstruction
- archival workflows
- cross‑platform development environments
