#!/usr/bin/env bash

XDG_RUNTIME_DIR=/tmp/runtime-root exec /usr/bin/calibre-server \
    --disable-use-bonjour \
    --enable-local-write \
    --listen-on 127.0.0.1 \
    --auth-mode=basic \
    "$@" \
    "/library"
