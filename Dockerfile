FROM fedora:latest

RUN dnf update -y \
	&& dnf install --nodocs -y flatpak flatpak-builder \
	&& dnf clean all
