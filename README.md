# RemoveSamples - NZBGet Extension

[![Tests](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml)
[![Prospector](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml)
[![Manifest Check](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml)

NZBGet extension to detect and delete sample files/directories before Sonarr/Radarr/Lidarr/Prowlarr processing.

## Features

- 🎯 **Smart Detection**: Identifies sample files by name patterns and size thresholds
- 📁 **Directory Cleanup**: Removes entire sample directories
- 🎬 **Video Support**: Configurable size limits for various video formats
- 🎵 **Audio Support**: Handles audio sample detection
- ⚙️ **Easy Configuration**: Modern dropdown interface for settings
- 🔧 **Flexible**: Enable/disable file or directory removal independently

## Installation

### Via NZBGet Extension Manager (Recommended)
1. Open NZBGet web interface
2. Go to **Settings** → **Extension Manager**
3. Find "Remove Samples" in the list
4. Click **Install**

### Manual Installation
1. Download the latest release
2. Extract to your NZBGet scripts directory: `/path/to/nzbget/scripts/RemoveSamples/`
3. Set execute permissions (Linux/Unix only): `chmod 755 main.py`
4. Restart NZBGet

## Configuration

### Basic Options (Dropdown Selectors)
- **Remove Directories**: Delete folders whose names match "sample" (Yes/No)
- **Remove Files**: Delete files whose names contain "sample" (Yes/No)  
- **Debug**: Enable verbose debug logging (Yes/No)

### Advanced Options
- **Video Size Threshold**: Size limit (MB) to treat video as sample
  - 50 MB ≈ 720p clip
  - 100 MB ≈ 1080p clip  
  - 150 MB ≈ 2160p clip
- **Video Extensions**: Comma-separated list of video file extensions
- **Audio Size Threshold**: Size limit (MB) to treat audio as sample
  - 2 MB ≈ 30 seconds of 320 kbps MP3
  - Set to 0 to disable size-based audio detection
- **Audio Extensions**: Comma-separated list of audio file extensions

## Usage

1. **Configure the extension** in Settings → Extension Manager → Remove Samples
2. **Assign to categories** in Settings → Categories → select "RemoveSamples" in ExtensionScripts
3. **Set script order** carefully within your workflow for optimal results

## Sample Detection Logic

The extension identifies samples using multiple criteria:

### File Name Patterns
- Contains "sample" as a word boundary
- Patterns like `.sample.`, `_sample.`, `-sample.`, `sample_`, `sample-`
- Files starting with "sample."

### Directory Name Patterns  
- Directory names containing "sample" or "samples"
- Exact matches for "sample" or "samples"

### Size-Based Detection
- **Video files**: Below configured threshold (default 150MB)
- **Audio files**: Below configured threshold (default 2MB)
- Only applies to files with matching extensions

## Examples

### What Gets Removed
✅ `Movie.Name.2023.sample.mkv`  
✅ `sample.mp4`  
✅ `preview_sample.avi`  
✅ `samples/` directory  
✅ Small video files under threshold  

### What Gets Preserved
❌ `Movie.Name.2023.1080p.mkv` (normal size)  
❌ `soundtrack.mp3` (no sample pattern)  
❌ `behind-the-scenes.mp4` (above threshold)  

## Requirements

- **NZBGet**: Version 14.0 or later
- **Python**: 3.8+ installed on your system
- **Permissions**: Execute permission on main.py

## Workflow Integration

Place RemoveSamples strategically in your post-processing workflow:

```
Download → RemoveSamples → Unpack → Other Scripts → Sonarr/Radarr/Lidarr/Prowlarr
```

**Example workflow order:**
```
PasswordDetector → FakeDetector → RemoveSamples → Clean
```

This ensures samples are removed before media managers (Sonarr/Radarr/Lidarr/Prowlarr) process the files.

## Troubleshooting

### Extension Not Appearing
- Check that both `main.py` and `manifest.json` are in the correct directory
- Verify execute permissions: `ls -la main.py`
- Restart NZBGet after installation

### Files Not Being Removed
- Enable Debug mode to see detailed logs
- Check file/directory patterns match detection logic
- Verify size thresholds are appropriate for your content

### Permission Errors
```bash
chmod 755 /path/to/nzbget/scripts/RemoveSamples/main.py
```

## Development

### Running Tests
```bash
python -m unittest tests.py -v
```

### Code Quality
```bash
pip install prospector
prospector main.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

GNU General Public License v2.0 - see LICENSE file for details.

## Support

- **Issues**: Report bugs or request features via GitHub Issues
- **Discussions**: General questions and community support via GitHub Discussions

## Changelog

### v1.0.0
- Initial release with modern NZBGet extension format
- Dropdown configuration interface
- Comprehensive sample detection
- Configurable video/audio thresholds
- Full test coverage