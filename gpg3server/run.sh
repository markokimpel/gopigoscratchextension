#!/bin/sh

# Start GoPiGo3 Server.

# Make this folder current folder.
cd "$(dirname "$0")"
python3 gpg3server.py
