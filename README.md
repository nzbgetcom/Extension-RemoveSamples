# RemoveSamples - NZBGet Extension

[![Tests](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/tests.yml)
[![Prospector](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/prospector.yml)
[![Manifest Check](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml/badge.svg)](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/actions/workflows/manifest.yml)

**Modern NZBGet extension** for intelligent sample file detection and removal. Automatically cleans sample files and directories before Sonarr/Radarr/Lidarr/Prowlarr processing.

> 🔄 **Replaces the legacy DeleteSamples.py script** with modern extension format and advanced detection algorithms.

## 🚀 Quick Start

**📖 [Complete Documentation](../../wiki)** | **🚀 [Installation Guide](../../wiki/Installation-Guide)** | **⚙️ [Configuration Reference](../../wiki/Configuration-Reference)**

## ✨ Key Features

- 🎯 **Smart Detection**: Advanced pattern matching with word boundary detection
- 📁 **Directory Cleanup**: Removes entire sample directories (`samples/`, `SAMPLE/`)
- 🎬 **Video Support**: Configurable size thresholds for different quality levels
- 🎵 **Audio Support**: Separate detection logic for audio samples
- ⚙️ **Modern Interface**: GUI dropdown configuration (no file editing!)
- 🐳 **Docker Ready**: Works with all popular NZBGet Docker containers
- 🔧 **Flexible**: Independent control over file and directory removal
- 🛡️ **Enterprise-Grade**: Automated security scanning and dependency monitoring

## 🆚 Why Choose RemoveSamples?

**vs DeleteSamples.py (Legacy Script)**

| Feature | DeleteSamples.py | RemoveSamples |
|---------|-----------------|---------------|
| **Configuration** | ❌ Manual file editing | ✅ Modern dropdown interface |
| **Directory Removal** | ❌ Files only | ✅ Files AND directories |
| **Extension Format** | ❌ Legacy script | ✅ Modern NZBGet extension |
| **Pattern Detection** | ❌ Basic substring | ✅ Advanced pattern matching |
| **Audio Support** | ❌ Limited | ✅ Full configurable support |
| **Maintenance** | ❌ Abandoned (6+ years) | ✅ Active development |

**[See detailed comparison →](../../wiki/Comparison-DeleteSamples)**

## 📦 Installation

### Method 1: Extension Manager (Recommended)
1. Open NZBGet web interface
2. Go to **Settings** → **Extension Manager**
3. Find "RemoveSamples" in the list
4. Click **Install**

### Method 2: Manual Installation
```bash
# Download and extract to NZBGet scripts directory
mkdir -p /path/to/nzbget/scripts/RemoveSamples/
# Copy main.py and manifest.json
chmod 755 main.py && chmod 644 manifest.json
```

### Method 3: Docker/Unraid
```bash
# For Unraid NZBGet containers
cd /mnt/user/appdata/nzbget/scripts/
mkdir -p RemoveSamples
# Download files and set permissions for nobody:users
```

**📖 [Detailed installation instructions for all platforms →](../../wiki/Installation-Guide)**

## ⚙️ Configuration

### Basic Settings (Dropdown Interface)
```
Remove Directories: Yes    # Delete sample directories
Remove Files: Yes          # Delete sample files  
Debug: No                  # Enable for troubleshooting
```

### Advanced Thresholds
```
Video Size Threshold: 150 MB    # 720p: 50MB, 1080p: 100MB, 4K: 300MB+
Audio Size Threshold: 2 MB      # ~30 seconds of 320kbps MP3
```

### Recommended Settings by Use Case

**Conservative (New Users)**
```
Video: 300 MB | Audio: 5 MB | Debug: Yes
```

**Balanced (Most Users)**
```
Video: 150 MB | Audio: 2 MB | Debug: No
```

**Aggressive (High Volume)**
```
Video: 50 MB | Audio: 1 MB | Debug: No
```

**📖 [Complete configuration guide →](../../wiki/Configuration-Reference)**

## 🔄 Workflow Integration

### Recommended Script Order
```
1. PasswordDetector (if used)
2. FakeDetector (if used)
3. RemoveSamples ← Place here
4. Clean (if used)
5. Other scripts
```

### Media Manager Integration
- **Sonarr**: Cleaner TV episode imports, no sample episodes
- **Radarr**: No trailer/sample files in movie folders  
- **Lidarr**: No 30-second preview tracks in albums
- **Prowlarr**: Consistent cleanup across all content types

**📖 [Complete workflow integration guide →](../../wiki/Workflow-Integration)**

## 📊 Sample Detection Examples

### ✅ Will Be Removed
```
Movie.Name.2023.sample.mkv      # Pattern + size match
sample.mp4                      # Clear sample file
preview_sample.avi              # Sample pattern
samples/                        # Sample directory
Small.video.under.150MB.mkv     # Size-based detection
```

### ❌ Will Be Preserved  
```
Movie.Name.2023.1080p.mkv       # Normal size, no pattern
soundtrack.mp3                  # No sample pattern
behind-the-scenes.mp4           # Above size threshold
Movie.Title.SAMPLE.2023.mkv     # If "SAMPLE" in original title
```

## 🔍 Detection Logic

### Pattern Matching
- **Word boundary detection**: `\bsample\b` prevents false positives
- **Multiple separators**: `.sample.`, `_sample.`, `-sample.`
- **Directory patterns**: Comprehensive sample directory detection

### Size-Based Detection
- **Separate thresholds** for video/audio files
- **Configurable extensions** for each media type
- **Smart combination** of pattern and size detection

**📖 [Complete detection logic documentation →](../../wiki/Detection-Logic)**

## 🐳 Docker & Container Support

**Fully compatible with popular Docker containers:**
- ✅ `linuxserver/nzbget` (Recommended)
- ✅ `nzbget/nzbget` (Official)
- ✅ Unraid Community Applications NZBGet
- ✅ Custom Docker Compose setups

**Container-specific installation guides available in documentation.**

## 🚨 Troubleshooting

### Quick Diagnostics
```bash
# Enable debug mode
Settings → Extension Manager → RemoveSamples → Debug: Yes

# Check logs
Settings → Logging → Messages

# Verify installation
ls -la /path/to/scripts/RemoveSamples/
# Should show: main.py (executable) and manifest.json
```

### Common Issues
- **Extension not appearing**: Check file permissions and restart NZBGet
- **Files not removed**: Verify thresholds and enable debug mode
- **Docker permissions**: Use container-appropriate user/group

**📖 [Complete troubleshooting guide →](../../wiki/Troubleshooting-Guide)**

## 📞 Support & Documentation

- **📖 Complete Wiki**: [Comprehensive Documentation](../../wiki)
- **🐛 Bug Reports**: [GitHub Issues](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/issues)
- **💬 Discussions**: [GitHub Discussions](https://github.com/Anunnaki-Astronaut/RemoveSamples-NZBGet/discussions)
- **🔒 Security Issues**: anunnaki.astronaut@machinamindmeld.com
- **❓ FAQ**: [Frequently Asked Questions](../../wiki/FAQ)

## 🛡️ Security & Quality

RemoveSamples is built with enterprise-grade practices:
- **Automated security scanning** with CodeQL
- **Dependency vulnerability monitoring** with Dependabot
- **Comprehensive test coverage** with automated CI/CD
- **Professional code review** workflow

## 🏆 Recognition

*Submitted to NZBGet team for inclusion in the official extension repository.*

## 📋 Requirements

- **NZBGet**: Version 14.0 or later (21.0+ recommended)
- **Python**: 3.8+ installed on your system
- **Permissions**: Execute permission on main.py

## 🔧 Development

### Running Tests
```bash
python -m unittest tests.py -v
```

### Code Quality Checks
```bash
pip install prospector
prospector main.py
```

### Contributing
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes with tests
4. Ensure all tests pass: `python -m unittest tests.py -v`
5. Submit a pull request

**📖 [Development documentation →](../../wiki/Contributing)**

## 📄 License

GNU General Public License v2.0 - see [LICENSE](LICENSE) file for details.

## 📈 Changelog

### v1.0.0 - Initial Release
- ✅ Modern NZBGet extension format with manifest.json
- ✅ GUI dropdown configuration interface  
- ✅ Advanced pattern matching with word boundaries
- ✅ Comprehensive sample detection (files + directories)
- ✅ Configurable video/audio size thresholds
- ✅ Full test coverage with automated CI/CD
- ✅ Docker and Unraid compatibility
- ✅ Enterprise-grade security practices
- ✅ Complete documentation wiki

---

**Ready to get started?** → **[Installation Guide](../../wiki/Installation-Guide)**  
**Need help?** → **[FAQ](../../wiki/FAQ)** | **[Troubleshooting](../../wiki/Troubleshooting-Guide)**