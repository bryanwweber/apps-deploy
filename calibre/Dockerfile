# syntax=docker/dockerfile:1
FROM curlimages/curl-base:latest AS base
ARG CALIBRE_VERSION=8.5.0

RUN apk add --no-cache xz tar

RUN curl -fsSL -o /tmp/calibre-tarball.txz https://download.calibre-ebook.com/${CALIBRE_VERSION}/calibre-${CALIBRE_VERSION}-x86_64.txz \
    && mkdir -p /opt/calibre \
    && tar -xJvf /tmp/calibre-tarball.txz -C /opt/calibre \
    && rm /tmp/calibre-tarball.txz

FROM ubuntu:noble-20250415.1 AS final

ENV XDG_RUNTIME_DIR=/tmp/runtime-root
COPY --from=base /opt/calibre /opt/calibre

RUN --mount=target=/var/lib/apt/lists,type=cache,sharing=locked \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    rm -f /etc/apt/apt.conf.d/docker-clean \
    && apt-get update \
    && apt-get install -y \
    dbus \
    dnsutils \
    fcitx-rime \
    fonts-wqy-microhei \
    iproute2 \
    libfontconfig \
    libgl1 \
    libnss3 \
    libopengl0 \
    libqpdf29t64 \
    libxcb-cursor0 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxkbcommon-x11-0 \
    poppler-utils \
    tini \
    && /opt/calibre/calibre_postinstall \
    && mkdir /library \
    && useradd --system --create-home --shell /bin/bash calibre \
    && chown -R calibre:calibre /opt/calibre \
    && chown -R calibre:calibre /library \
    && touch /var/log/calibre.log \
    && chown calibre:calibre /var/log/calibre.log

USER calibre

EXPOSE 8080
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/usr/bin/calibre-server", "--access-log=/var/log/calibre.log", "--disable-use-bonjour", "--trusted-ips=0.0.0.0", "--enable-local-write", "--listen-on", "0.0.0.0", "--auth-mode=basic", "--url-prefix", "/calibre", "/library" ]
