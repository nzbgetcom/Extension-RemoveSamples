#!/usr/bin/env python3
##############################################################################
# Title : RemoveSamples.py
# Author: Anunnaki-Astronaut
# URL   : https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###
#
# Detects and deletes "sample" files and/or directories in a download
# before Sonarr / Radarr / Lidarr / Prowlarr see them.
#
# 1. In NZBGet ► Settings ► CATEGORIES select "RemoveSamples" in
#    "ExtensionScripts" for every category you want cleaned.
# 2. Script order: place RemoveSamples carefully within your workflow for
#    optimal results.
#
# NOTE: This script requires Python to be installed in the container/host.
#
##############################################################################
### NZBGET POST-PROCESSING SCRIPT                                          ###
##############################################################################

import os
import sys
import shutil
import re
import pathlib

# --- NZBGet exit codes -----------------------------------------------------
POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR   = 94
POSTPROCESS_NONE    = 95

print("[DETAIL] RemoveSamples extension started")
sys.stdout.flush()

# Check required options
required_options = (
    "NZBPO_REMOVEDIRECTORIES",
    "NZBPO_REMOVEFILES", 
    "NZBPO_DEBUG",
    "NZBPO_VIDEOSIZETHRESHOLDMB",
    "NZBPO_VIDEOEXTS",
    "NZBPO_AUDIOSIZETHRESHOLDMB",
    "NZBPO_AUDIOEXTS"
)

for optname in required_options:
    if optname not in os.environ:
        print(f"[ERROR] Option {optname[6:]} is missing in configuration file. Please check script settings")
        sys.exit(POSTPROCESS_ERROR)

# ── Read NZBGet variables & user options ───────────────────────────────────
DEBUG       = os.environ.get('NZBPO_DEBUG', 'No').lower() in ('yes', 'y', 'true', '1')
REM_DIRS    = os.environ.get('NZBPO_REMOVEDIRECTORIES','Yes').lower() in ('yes', 'y', 'true', '1')
REM_FILES   = os.environ.get('NZBPO_REMOVEFILES','Yes').lower() in ('yes', 'y', 'true', '1')

VID_LIMIT   = int(os.environ.get('NZBPO_VIDEOSIZETHRESHOLDMB','150') or '0')
AUD_LIMIT   = int(os.environ.get('NZBPO_AUDIOSIZETHRESHOLDMB','2')   or '0')

VIDEO_EXTS  = {e if e.startswith('.') else f'.{e}'
               for e in os.environ.get(
                   'NZBPO_VIDEOEXTS',
                   '.mkv,.mp4,.avi,.mov,.wmv,.flv,.webm,.ts,.m4v,.vob'
               ).split(',') if e.strip()}

AUDIO_EXTS  = {e if e.startswith('.') else f'.{e}'
               for e in os.environ.get(
                   'NZBPO_AUDIOEXTS',
                   '.wav,.aiff,.mp3,.flac,.m4a,.ogg,.aac,.alac,.ape,.opus,.wma'
               ).split(',') if e.strip()}

DL_DIR      = os.environ.get('NZBPP_DIRECTORY')
DL_STATUS   = os.environ.get('NZBPP_STATUS', '')
DL_NAME     = os.environ.get('NZBPP_NZBNAME', '')

log = lambda lvl, m: print(f"[{lvl}] {m}")
dbg = lambda m: DEBUG and log("DEBUG", m)

# ── Regex patterns ─────────────────────────────────────────────────────────
FILE_RE = [re.compile(p, re.I) for p in (
    r'\bsample\b', r'\.sample\.', r'^sample\.', r'_sample\.', r'-sample\.',
    r'sample[_-]'
)]
DIR_RE  = [re.compile(p, re.I) for p in (r'\bsamples?\b', r'^samples?$')]

# ── Sample detection helpers ───────────────────────────────────────────────
def is_sample_file(path: pathlib.Path) -> bool:
    name = path.name
    if any(r.search(name) for r in FILE_RE):
        return True
    ext = path.suffix.lower()
    try:
        size_mb = path.stat().st_size / (1 << 20)
    except OSError:
        return False

    if ext in VIDEO_EXTS and VID_LIMIT and size_mb <= VID_LIMIT:
        return True
    if ext in AUDIO_EXTS and AUD_LIMIT and size_mb <= AUD_LIMIT:
        return True
    return False

def is_sample_dir(dir_name: str) -> bool:
    return any(r.search(dir_name) for r in DIR_RE)

def remove_samples(root: pathlib.Path):
    removed = []
    for p in sorted(root.rglob('*'), reverse=True):
        if p.is_file() and REM_FILES and is_sample_file(p):
            p.unlink(missing_ok=True)
            removed.append(str(p))
            log("INFO", f"Removed file {p.relative_to(root)}")
        elif p.is_dir() and REM_DIRS and is_sample_dir(p.name):
            shutil.rmtree(p, ignore_errors=True)
            removed.append(str(p))
            log("INFO", f"Removed dir  {p.relative_to(root)}")
    return removed

# ── Main entry ─────────────────────────────────────────────────────────────
def main():
    # Check if running in post-processing mode
    if not DL_DIR:
        log("ERROR", "NZBPP_DIRECTORY missing - script must run in post-processing mode")
        sys.exit(POSTPROCESS_ERROR)

    if not DL_STATUS.upper().startswith('SUCCESS'):
        log("INFO", f"Status {DL_STATUS}; skipping.")
        sys.exit(POSTPROCESS_NONE)

    if not os.path.exists(DL_DIR):
        log("ERROR", f"Destination directory doesn't exist: {DL_DIR}")
        sys.exit(POSTPROCESS_NONE)

    log("INFO", f"Processing \"{DL_NAME}\" in {DL_DIR}")
    dbg(f"dirs={REM_DIRS}, files={REM_FILES}, "
        f"vid≤{VID_LIMIT} MB, aud≤{AUD_LIMIT} MB, "
        f"vExt={sorted(VIDEO_EXTS)}, aExt={sorted(AUDIO_EXTS)}")

    removed_count = len(remove_samples(pathlib.Path(DL_DIR)))
    log("INFO", f"Removed {removed_count} sample item(s)")
    
    print("[DETAIL] RemoveSamples extension completed successfully")
    sys.exit(POSTPROCESS_SUCCESS)

if __name__ == '__main__':
    main()