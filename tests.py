#!/usr/bin/env python3
#
# Tests for RemoveSamples Extension
#
# Copyright (C) 2025 Anunnaki-Astronaut
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#

import sys
import unittest
import shutil
import os
import subprocess
import pathlib
import tempfile
from os.path import dirname

ROOT_DIR = dirname(__file__)

POSTPROCESS_SUCCESS = 93
POSTPROCESS_ERROR = 94
POSTPROCESS_NONE = 95

def get_python():
    if os.name == "nt":
        return "python"
    return "python3"

def set_defaults(test_dir):
    """Set default environment variables for testing"""
    os.environ["NZBPO_REMOVEDIRECTORIES"] = "Yes"
    os.environ["NZBPO_REMOVEFILES"] = "Yes"
    os.environ["NZBPO_DEBUG"] = "No"
    os.environ["NZBPO_VIDEOSIZETHRESHOLDMB"] = "150"
    os.environ["NZBPO_VIDEOEXTS"] = ".mkv,.mp4,.avi,.mov,.wmv,.flv,.webm,.ts,.m4v,.vob"
    os.environ["NZBPO_AUDIOSIZETHRESHOLDMB"] = "2"
    os.environ["NZBPO_AUDIOEXTS"] = ".wav,.aiff,.mp3,.flac,.m4a,.ogg,.aac,.alac,.ape,.opus,.wma"
    os.environ["NZBPP_DIRECTORY"] = test_dir
    os.environ["NZBPP_STATUS"] = "SUCCESS"
    os.environ["NZBPP_NZBNAME"] = "Test.Download"

def run_script():
    """Run the main.py script and return output, return code, and error"""
    sys.stdout.flush()
    proc = subprocess.Popen(
        [get_python(), ROOT_DIR + "/main.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=os.environ.copy(),
    )
    out, err = proc.communicate()
    ret_code = proc.returncode
    return (out.decode(), int(ret_code), err.decode())

class TestRemoveSamples(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        set_defaults(self.test_dir)
    
    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_script_success(self):
        """Test that script runs successfully with default settings"""
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertIn("RemoveSamples extension started", output)
        self.assertIn("RemoveSamples extension completed successfully", output)
    
    def test_missing_directory(self):
        """Test script behavior when download directory doesn't exist"""
        os.environ["NZBPP_DIRECTORY"] = "/nonexistent/directory"
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_NONE)
        self.assertIn("doesn't exist", output)
    
    def test_sample_file_detection(self):
        """Test that sample files are properly detected"""
        # Create test files
        test_file = pathlib.Path(self.test_dir) / "sample.mkv"
        test_file.write_text("test content")
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertFalse(test_file.exists())  # Should be removed
    
    def test_sample_directory_detection(self):
        """Test that sample directories are properly detected"""
        # Create test directory
        sample_dir = pathlib.Path(self.test_dir) / "samples"
        sample_dir.mkdir()
        (sample_dir / "test.txt").write_text("test content")
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertFalse(sample_dir.exists())  # Should be removed
    
    def test_small_video_file_detection(self):
        """Test that small video files are detected as samples"""
        # Create small video file (under threshold)
        small_video = pathlib.Path(self.test_dir) / "movie.mkv"
        small_video.write_bytes(b"x" * 1024)  # 1KB file, well under 150MB threshold
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertFalse(small_video.exists())  # Should be removed as sample
    
    def test_normal_files_preserved(self):
        """Test that normal files are not removed"""
        # Create normal file
        normal_file = pathlib.Path(self.test_dir) / "movie.mkv"
        normal_file.write_bytes(b"x" * (200 * 1024 * 1024))  # 200MB file, over threshold
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertTrue(normal_file.exists())  # Should be preserved
    
    def test_disabled_file_removal(self):
        """Test that file removal can be disabled"""
        os.environ["NZBPO_REMOVEFILES"] = "No"
        
        # Create sample file
        sample_file = pathlib.Path(self.test_dir) / "sample.mkv"
        sample_file.write_text("test content")
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertTrue(sample_file.exists())  # Should be preserved when disabled
    
    def test_disabled_directory_removal(self):
        """Test that directory removal can be disabled"""
        os.environ["NZBPO_REMOVEDIRECTORIES"] = "No"
        
        # Create sample directory
        sample_dir = pathlib.Path(self.test_dir) / "samples"
        sample_dir.mkdir()
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_SUCCESS)
        self.assertTrue(sample_dir.exists())  # Should be preserved when disabled
    
    def test_failed_status_skip(self):
        """Test that script skips processing when status is not SUCCESS"""
        os.environ["NZBPP_STATUS"] = "FAILURE"
        
        [output, code, error] = run_script()
        self.assertEqual(code, POSTPROCESS_NONE)
        self.assertIn("skipping", output)

if __name__ == "__main__":
    unittest.main()