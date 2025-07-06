#!/usr/bin/env python3
"""RemoveSamples NZBGet Extension.

Modern NZBGet extension for intelligent sample file detection and removal.
Automatically cleans sample files and directories before Sonarr/Radarr/Lidarr/Prowlarr processing.

Repository: https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet
Documentation: https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/wiki
"""

##############################################################################
# Title: RemoveSamples.py
# Author: Anunnaki-Astronaut  
# URL: https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet
# License: GNU General Public License v2.0
# v1.0.1 - Ready for NZBGet team review
##############################################################################
# NZBGET POST-PROCESSING SCRIPT
#
# RemoveSamples - Modern NZBGet Extension
#
# Intelligently detects and removes sample files and directories using:
# • Advanced pattern matching with word boundary detection
# • Configurable size thresholds for video/audio files  
# • Comprehensive sample directory cleanup
# • GUI dropdown configuration (no file editing required)
#
# 🎯 QUICK SETUP:
# 1. Settings → Categories → [Your Category] → ExtensionScripts → Add "RemoveSamples"
# 2. Place RemoveSamples AFTER unpack but BEFORE media manager processing
# 3. Configure thresholds: 720p=50MB, 1080p=150MB, 4K=300-500MB
#
# 📖 Complete documentation and troubleshooting:
# https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/wiki
#
# 🔄 Replaces legacy DeleteSamples.py with modern extension format
#
##############################################################################

import os
import re
import shutil
import sys
from pathlib import Path

# NZBGet exit codes
POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95

print("[DETAIL] RemoveSamples v1.0.1 extension started")
sys.stdout.flush()

# Check required configuration options
REQUIRED_OPTIONS = (
    "NZBPO_REMOVEDIRECTORIES",
    "NZBPO_REMOVEFILES", 
    "NZBPO_DEBUG",
    "NZBPO_VIDEOSIZETHRESHOLDMB",
    "NZBPO_VIDEOEXTS",
    "NZBPO_AUDIOSIZETHRESHOLDMB",
    "NZBPO_AUDIOEXTS"
)

for optname in REQUIRED_OPTIONS:
    if optname not in os.environ:
        error_msg = (
            f"[ERROR] Configuration option {optname[6:]} is missing. "
            f"Please check RemoveSamples settings in Extension Manager."
        )
        print(error_msg)
        sys.exit(POSTPROCESS_ERROR)

# Read NZBGet variables and user configuration
DEBUG = os.environ.get('NZBPO_DEBUG', 'No').lower() in (
    'yes', 'y', 'true', '1'
)
REM_DIRS = os.environ.get('NZBPO_REMOVEDIRECTORIES', 'Yes').lower() in (
    'yes', 'y', 'true', '1'
)
REM_FILES = os.environ.get('NZBPO_REMOVEFILES', 'Yes').lower() in (
    'yes', 'y', 'true', '1'
)

# Size thresholds (MB)
VID_LIMIT = int(os.environ.get('NZBPO_VIDEOSIZETHRESHOLDMB', '150') or '0')
AUD_LIMIT = int(os.environ.get('NZBPO_AUDIOSIZETHRESHOLDMB', '2') or '0')

# File extensions (normalize to include leading dots)
VIDEO_EXTS = {
    e if e.startswith('.') else f'.{e}'
    for e in os.environ.get(
        'NZBPO_VIDEOEXTS',
        '.mkv,.mp4,.avi,.mov,.wmv,.flv,.webm,.ts,.m4v,.vob,.mpg,.mpeg,.iso'
    ).split(',') if e.strip()
}

AUDIO_EXTS = {
    e if e.startswith('.') else f'.{e}'
    for e in os.environ.get(
        'NZBPO_AUDIOEXTS',
        '.mp3,.flac,.aac,.ogg,.wma,.m4a,.opus,.wav,.alac,.ape'
    ).split(',') if e.strip()
}

# NZBGet environment variables
DL_DIR = os.environ.get('NZBPP_DIRECTORY')
DL_STATUS = os.environ.get('NZBPP_STATUS', '')
DL_NAME = os.environ.get('NZBPP_NZBNAME', '')


def log(level, message):
    """Log a message with the specified level."""
    print(f"[{level}] RemoveSamples: {message}")


def debug_log(message):
    """Log a debug message if debug mode is enabled."""
    if DEBUG:
        log("DEBUG", message)


# Sample detection patterns
FILE_PATTERNS = [
    r'\bsample\b',      # Word boundary "sample" - prevents "resample" matches
    r'\.sample\.',      # .sample. in filename
    r'^sample\.',       # Starts with "sample."
    r'_sample\.',       # _sample. pattern
    r'-sample\.',       # -sample. pattern
    r'sample[_-]'       # sample followed by separator
]

DIR_PATTERNS = [
    r'\bsamples?\b',    # "sample" or "samples" as whole words
    r'^samples?$'       # Exact match "sample" or "samples"
]

# Compile regex patterns for performance
FILE_RE = [re.compile(pattern, re.IGNORECASE) for pattern in FILE_PATTERNS]
DIR_RE = [re.compile(pattern, re.IGNORECASE) for pattern in DIR_PATTERNS]


def is_sample_file(path):
    """Check if a file is considered a sample based on name and size."""
    name = path.name
    if any(regex.search(name) for regex in FILE_RE):
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


def is_sample_dir(dir_name):
    """Check if a directory name matches sample patterns."""
    return any(regex.search(dir_name) for regex in DIR_RE)


def remove_samples(root):
    """Remove sample files and directories from the specified root path."""
    removed = []
    for path in sorted(root.rglob('*'), reverse=True):
        if path.is_file() and REM_FILES and is_sample_file(path):
            path.unlink(missing_ok=True)
            removed.append(str(path))
            log("INFO", f"Removed file {path.relative_to(root)}")
        elif path.is_dir() and REM_DIRS and is_sample_dir(path.name):
            shutil.rmtree(path, ignore_errors=True)
            removed.append(str(path))
            log("INFO", f"Removed dir  {path.relative_to(root)}")
    return removed


def main():
    """Main entry point for the RemoveSamples extension."""
    # Check if running in post-processing mode
    if not DL_DIR:
        log("ERROR", "NZBPP_DIRECTORY missing - script must run in post-processing mode")
        sys.exit(POSTPROCESS_ERROR)

    if not DL_STATUS.upper().startswith('SUCCESS'):
        log("INFO", f"Download status '{DL_STATUS}' - skipping sample removal")
        sys.exit(POSTPROCESS_NONE)

    if not os.path.exists(DL_DIR):
        log("ERROR", f"Download directory does not exist: {DL_DIR}")
        sys.exit(POSTPROCESS_NONE)

    # Log processing start
    log("INFO", f"Processing '{DL_NAME}' in {DL_DIR}")
    
    # Log configuration (debug mode only)
    if DEBUG:
        config_info = (
            f"Configuration: RemoveDirectories={REM_DIRS}, RemoveFiles={REM_FILES}, "
            f"VideoThreshold={VID_LIMIT}MB, AudioThreshold={AUD_LIMIT}MB"
        )
        debug_log(config_info)
        debug_log(f"Video extensions: {sorted(VIDEO_EXTS)}")
        debug_log(f"Audio extensions: {sorted(AUDIO_EXTS)}")

    # Process the download directory
    try:
        removed_items = remove_samples(Path(DL_DIR))
        item_count = len(removed_items)
        
        if item_count > 0:
            log("INFO", f"Sample removal completed - removed {item_count} item(s)")
        else:
            log("INFO", "No sample files or directories found")
            
    except Exception as e:
        log("ERROR", f"Unexpected error during processing: {e}")
        sys.exit(POSTPROCESS_ERROR)

    print("[DETAIL] RemoveSamples extension completed successfully")
    sys.exit(POSTPROCESS_SUCCESS)


if __name__ == '__main__':
    main()