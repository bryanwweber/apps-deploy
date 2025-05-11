# syntax=docker/dockerfile:1

FROM curlimages/curl-base:latest AS base
ARG CALIBRE_VERSION=8.4.0

RUN apk add --no-cache xz tar

RUN curl -fsSL -o /tmp/calibre-tarball.txz https://download.calibre-ebook.com/${CALIBRE_VERSION}/calibre-${CALIBRE_VERSION}-x86_64.txz \
    && mkdir -p /opt/calibre \
    && tar -xJvf /tmp/calibre-tarball.txz -C /opt/calibre \
    && rm /tmp/calibre-tarball.txz

FROM ubuntu:noble-20250415.1 AS final

COPY --from=base /opt/calibre /opt/calibre
COPY start-calibre-server.sh .

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
    && touch /library/metadata.db

RUN useradd --system --no-create-home --shell /bin/bash calibre \
    && chown -R calibre:calibre /opt/calibre \
    && chown -R calibre:calibre /library
USER calibre

EXPOSE 8080
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/start-calibre-server.sh" ]
