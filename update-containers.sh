#!/bin/bash
set -euo pipefail

source ./versions.sh
docker compose -f docker-compose.yml pull
sudo systemctl restart apps-deploy.service
