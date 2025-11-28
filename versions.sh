# These versions are apps that aren't built locally and need to be specified.
# Caddy and Calibre versions are specified in the docker-bake.hcl configuration.
while IFS='|' read -r key value; do
    export "${key}=${value}"
done < <(/usr/bin/docker buildx bake --progress quiet --file docker-bake.hcl --print \
    | jq -r '.target[] | .args | to_entries[] | "\(.key)|\(.value)"')
export ATUIN_VERSION=18.8.0
export KARAKEEP_VERSION=0.28.0
export KOSYNCSERVER_VERSION=1.2.1
export TAILSCALE_VERSION=v1.90.9
export POSTGRES_VERSION=18.1
