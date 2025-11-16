#!/bin/bash
set -euo pipefail

while IFS= read -r line; do
        echo "Setting environment variable: $line"
        eval "$line"
done < <(docker buildx bake --file docker-bake.hcl --print \
    | jq '.target[] | .args | to_entries[] | "export \(.key)=\"\(.value)\""')
source ./versions.sh
docker compose -f docker-compose.yml pull
systemctl restart apps-deploy
