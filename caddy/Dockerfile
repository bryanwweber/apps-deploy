ARG CADDY_VERSION
FROM caddy:${CADDY_VERSION}-builder-alpine AS builder
ARG CADDY_DNS_NAMECHEAP_VERSION

RUN xcaddy build \
    --with github.com/caddy-dns/namecheap@v${CADDY_DNS_NAMECHEAP_VERSION}

FROM caddy:${CADDY_VERSION}-alpine AS final

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
COPY ./conf/Caddyfile /etc/caddy/Caddyfile
