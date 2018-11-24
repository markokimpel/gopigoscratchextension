#!/bin/bash

# Make this folder current folder.
cd "$(dirname "$0")"

# Write systemd unit file.
# Run service as the user that owns the file (typically 'pi').
sudo bash -c "echo '[Unit]
Description=GoPiGo3 Server
After=multi-user.target

[Service]
Type=idle
User=$(stat -c '%U' run.sh)
Group=$(stat -c '%G' run.sh)
ExecStart=$(pwd)/run.sh

[Install]
WantedBy=multi-user.target' >/etc/systemd/system/gpg3server.service"

# Make sure file permissions are 644.
sudo chown 644 /etc/systemd/system/gpg3server.service

# Reload service definitions.
sudo systemctl daemon-reload

echo "Service gpg3server has been installed."
