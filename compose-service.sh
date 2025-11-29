#!/bin/bash
set -euo pipefail
# Create a systemd service that autostarts & manages a docker-compose instance in the current directory
# by Uli Köhler - https://techoverflow.net
# Licensed as CC0 1.0 Universal

SERVICENAME="apps-deploy"

echo "Creating systemd service... /etc/systemd/system/${SERVICENAME}.service"
# Create systemd service file
sudo tee /etc/systemd/system/${SERVICENAME}.service > /dev/null <<EOF
[Unit]
Description=Start docker compose applications for $(basename "$(pwd)")
Requires=docker.service
After=docker.service

[Service]
Type=simple
Restart=always
User=apps-deploy
Group=docker
TimeoutStopSec=15
WorkingDirectory=$(pwd)
# Shutdown container (if running) when unit is started
ExecStartPre=/bin/bash -c 'source versions.sh && exec /usr/bin/docker compose -f docker-compose.yml down'
# Start container when unit is started
ExecStart=/bin/bash -c 'source versions.sh && exec /usr/bin/docker compose -f docker-compose.yml up'
# Stop container when unit is stopped
ExecStop=/bin/bash -c 'source versions.sh && exec /usr/bin/docker compose -f docker-compose.yml down'

[Install]
WantedBy=multi-user.target
EOF

echo "Enabling & starting $SERVICENAME"
# Autostart systemd service
sudo systemctl enable "${SERVICENAME}.service"
# Start systemd service now
sudo systemctl start "${SERVICENAME}.service"
