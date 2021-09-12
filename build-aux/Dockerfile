# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

FROM fedora:latest

RUN dnf update -y \
	&& dnf install --setopt=install_weak_deps=False --nodocs -y flatpak flatpak-builder git python3-pyyaml gzip brotli \
	&& dnf clean all
