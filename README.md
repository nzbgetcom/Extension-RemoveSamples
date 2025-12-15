# Remove Samples • NZBGet Extension

[![Tests](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml)
[![Prospector](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml)
[![Manifest Check](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml)

NZBGet extension that removes "sample" files and folders before Sonarr/Radarr/Lidarr/Prowlarr see the download. Keeps your library clean while protecting real content with conservative defaults.

---

## Overview

Scene releases often include short sample clips, promo images, and other junk alongside the real media. If those make it into your library you get:

* noisy episode/movie folders
* extra files in Plex/Jellyfin/Kodi
* higher chance of grabbing the wrong file in manual imports

**Remove Samples** runs after unpacking and before your media managers. It identifies sample-like content using filename patterns, size thresholds, and optional relative-size rules, then removes (or quarantines) the junk so only real media moves downstream.

---

## Key features

* **Sample-aware filename matching**
  Detects common patterns like `sample`, `SAMPLE`, `.sample.`, `_sample_`, etc., using word- and separator-aware matching to avoid false positives.

* **Size-based detection for video & audio**
  Treats very small video and audio files under your thresholds as samples (e.g. tiny preview clips).

* **Relative Size % detection (optional)**
  Flags a video as a sample when its size is below a certain percentage of the largest video in the same download. This gives you dynamic thresholds that scale with the release.

* **Per-category overrides**
  Category-specific thresholds let you tune behavior differently for TV, movies, music, etc., while keeping safe global defaults.

* **Safety tools for testing and recovery**

  * **Test Mode** – dry-run logging that shows what *would* be removed without touching the files.
  * **Block Import During Test** – optional companion to Test Mode that tells NZBGet to report a failure so media managers don’t import during a test run.
  * **Quarantine Mode** – instead of deleting, moves samples to a `_samples_quarantine` subfolder for manual review.
  * **Quarantine Max Age** – optional automatic cleanup of old quarantine files after a configurable number of days.

* **Protected Paths & Deny Patterns**

  * **Protected paths/names** let you explicitly shield things like subtitles, artwork, or NFOs so they are never removed, even if they look like samples.
  * **Deny patterns** are a configurable list of extra patterns you always want treated as junk.

* **Image & extras cleanup (optional)**
  Optional toggles to remove common screenshot/image samples and other minor extras left behind by some releases.

---

## Install

**NZBGet → Settings → Extension Manager**

1. Find **Remove Samples** in the list.
2. Click the download/install icon.
3. That’s it.

---

## Basic configuration

**NZBGet → Settings → Extension Manager → Remove Samples**

For most users, the defaults are a safe starting point:

* **Video Size Threshold (MB):** `150`
  Small video files under this size are considered candidates for sample detection.
* **Audio Size Threshold (MB):** `2`
  Small audio files (e.g., preview tracks) are treated as samples.
* **Remove Directories:** `Yes`
  Removes entire folders that look like sample directories.
* **Remove Files:** `Yes`
  Removes individual files that match sample patterns.
* **Debug:** `No`
  Leave off for daily use. Turn on temporarily when tuning settings or diagnosing behavior.

### Recommended defaults & safety notes

* Start with the bundled defaults; they are intentionally conservative.
* **Relative Size %** defaults to **8%**, which provides a good balance for most content. Most users can leave this and **Category Thresholds** at their defaults.
* **Protected Paths** always win: if a file matches a protected pattern (for example `*.srt` for subtitles), it will **never** be removed, even if it also looks like a sample.
* When experimenting with new thresholds or patterns, enable **Test Mode** first so you can review log output before allowing deletions or quarantine moves.

---

## Extension order in NZBGet

**NZBGet → Settings → Categories → `<Your Category>`.Extensions**

Place **RemoveSamples** **after** unpacking and **before** any final cleanup or media managers.

**Example (working setup):**

1. **Completion** – Verifies download completeness before processing
2. **PasswordDetector** – Detects password-protected archives early
3. **FakeDetector** – Flags fake/corrupted releases
4. **ExtendedUnpacker** – Extracts nested zip/rar archives
5. **RemoveSamples** – Removes sample files/folders **after unpack**
6. **Clean** – Final tidy-up

**Why order matters**

* Remove Samples runs **after unpack**, so it can see real files.
* It runs **before Clean**, so samples are removed before final cleanup.
* Upstream detection scripts run first to catch bad releases early.

---

## Quick test / first-run checklist

**Recommended first step – Test Mode only**

1. In Extension Manager, set **Test Mode = Yes**.
2. (Optional) Enable **Block Import (Test Mode) = Yes** if you want to prevent Sonarr/Radarr/Lidarr/Prowlarr from seeing the test download.
3. Process a known-good test download.
4. Open **NZBGet → Messages** and review the log lines:

   * size checks for video/audio
   * matches on filename patterns
   * summary line showing how many files/dirs would be removed or quarantined
5. Once you’re satisfied, set **Test Mode = No** (and **Block Import (Test Mode) = No** if you enabled it) to allow real removals or quarantine moves.

**When to use Debug**

* Turn **Debug = Yes** **by itself** (with Test Mode left at `No`) when you need deeper, per-item decision details to understand *why* something was or wasn’t treated as a sample.
* After troubleshooting, set **Debug = No** again for normal operation.

---

## Detection logic (short)

* **Word-boundary matching:** uses patterns like `\bsample\b` to avoid false positives inside longer words.
* **Separator-aware:** catches `.sample.`, `_sample_`, `-sample-`, and similar separators in filenames.
* **Size checks:** very small video/audio files under your thresholds are considered sample candidates.
* **Relative-size checks (optional):** flags videos that are much smaller than the main video in the same download when Relative Size % is enabled.

---

## Windows debug console note

If you previously saw a Unicode/console encoding error with **Debug** enabled on Windows, update to the latest version via Extension Manager. The script now uses UTF-8 console output on Windows so Debug works normally.

---

## NZBGet versions / requirements

* **NZBGet:** v23+ recommended
* **Python:** 3.8+ (required)

---

## Support

* **Bug Reports**: [https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/issues](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/issues)
* **Discussions**: [https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/discussions](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/discussions)

---

## License

**GNU General Public License v2.0** – see the LICENSE file for details.