# This file must be processed by 1Password CLI to fill in the templated variables
# We don't care about unused variables in this file
# shellcheck disable=2034

# Tailscale (common)
TS_AUTHKEY="op://App Deployment/Tailscale AuthKey/credential"

# Atuin
ATUIN_DB_NAME="op://App Deployment/Atuin DB Password/db name"
ATUIN_DB_USERNAME="op://App Deployment/Atuin DB Password/username"
ATUIN_DB_PASSWORD="op://App Deployment/Atuin DB Password/password"

# Caddy
NAMECHEAP_API_KEY="op://App Deployment/Namecheap API Key/credential"
NAMECHEAP_API_USER="op://App Deployment/Namecheap API Key/username"
CADDY_CONFIG_ROOT=${CADDY_CONFIG_ROOT:-./conf}
PUBLIC_CLIENT_IP=${PUBLIC_CLIENT_IP}

# Calibre
# The escaped space in the default value is needed so the Dotenv library that op uses
# can parse the file
CALIBRE_LIBRARY="${CALIBRE_LIBRARY:-/home/bweber/Calibre\ Library}"

# Forgejo
FORGEJO_DB_USERNAME="op://App Deployment/Forgejo DB/username"
FORGEJO_DB_NAME="op://App Deployment/Forgejo DB/db name"
FORGEJO_DB_PASSWORD="op://App Deployment/Forgejo DB/password"

# Karakeep
NEXTAUTH_SECRET="op://App Deployment/NextAuth Secret Token/credential"
MEILI_MASTER_KEY="op://App Deployment/Meili Master Key/credential"
OPENAI_API_KEY="op://App Deployment/OpenAI API Key/credential"
MEILI_ADDR=${MEILI_ADDR:-http://localhost:7700}
BROWSER_WEB_URL=${BROWSER_WEB_URL:-http://localhost:9222}
DATA_DIR=${DATA_DIR:-/data}
NEXTAUTH_URL=${NEXTAUTH_URL:-http://localhost:3000}
DISABLE_SIGNUPS=${DISABLE_SIGNUPS:-true}
CRAWLER_FULL_PAGE_ARCHIVE=${CRAWLER_FULL_PAGE_ARCHIVE:-true}
