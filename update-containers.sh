#!/bin/bash
set -euo pipefail

source ./versions.sh
docker compose -f docker-compose.yml pull
systemctl --user restart apps-deploy
