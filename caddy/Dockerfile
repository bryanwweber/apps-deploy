ARG CADDY_VERSION=2.10.2
FROM caddy:${CADDY_VERSION}-builder-alpine AS builder

RUN xcaddy build \
    --with github.com/caddy-dns/namecheap@master

FROM caddy:${CADDY_VERSION}-alpine AS final

COPY --from=builder /usr/bin/caddy /usr/bin/caddy
