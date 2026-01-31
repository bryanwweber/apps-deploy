group "default" {
  targets = ["calibre", "caddy"]
}

target "docker-metadata-action" {}

variable "CADDY_VERSION" {
  default = "2.10.2"
}

variable "CALIBRE_VERSION" {
  default = "9.1.0"
}

variable "UBUNTU_VERSION" {
  default = "noble-20251001"
}

target "caddy" {
  inherits = [ "docker-metadata-action" ]
  context = "caddy"
  dockerfile = "Dockerfile"
  args = {
    "CADDY_VERSION" = "${CADDY_VERSION}"
  }
  tags = [ "ghcr.io/bryanwweber/caddy:${CADDY_VERSION}", "ghcr.io/bryanwweber/caddy:latest" ]
  platforms = [ "linux/amd64", "linux/arm64" ]
  attest = [
    {
      type = "provenance"
      mode = "max"
    },
    {
      type = "sbom"
    }
  ]
}

target "calibre" {
  inherits = [ "docker-metadata-action" ]
  context = "calibre"
  dockerfile = "Dockerfile"
  args = {
    "CALIBRE_VERSION" = "${CALIBRE_VERSION}"
    "UBUNTU_VERSION" = "${UBUNTU_VERSION}"
  }
  tags = [ "ghcr.io/bryanwweber/calibre:${CALIBRE_VERSION}-${UBUNTU_VERSION}", "ghcr.io/bryanwweber/calibre:latest" ]
  platforms = [ "linux/amd64", "linux/arm64" ]
  labels = {
    "org.opencontainers.image.description" = "This image runs a Calibre server for managing eBooks."
    "org.opencontainers.image.licenses": "GPL-3.0"
    "org.opencontainers.image.title": "Calibre"
  }
  attest = [
    {
      type = "provenance"
      mode = "max"
    },
    {
      type = "sbom"
    }
  ]
}
