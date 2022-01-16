# SPDX-FileCopyrightText: 2021 Romain Vigier <contact AT romainvigier.fr>
# SPDX-License-Identifier: GPL-3.0-or-later

FROM registry.gitlab.com/rmnvgr/uishooter:latest

RUN dnf update -y \
	&& dnf install --setopt=install_weak_deps=False --nodocs -y git glib2-devel \
	&& dnf clean all

ENTRYPOINT [ "bash", "-c" ]
