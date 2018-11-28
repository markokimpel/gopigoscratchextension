#!/bin/sh

# Register GoPiGo3 scratch extension in Raspbian's Scratch 2 Offline Editor.
#
# Script needs to be run by user with sudo privileges.

# Make this folder current folder.
cd "$(dirname "$0")"

# Run Python install script.
sudo python3 install_extension.py
