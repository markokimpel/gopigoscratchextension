#!/bin/sh
# Make this folder current folder.
cd "$(dirname "$0")"
python3 streamingserver.py
