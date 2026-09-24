# SPDX-License-Identifier: GPL-3.0-or-later
#
# Copyright (C) 2025 Olliver Schinagl <oliver@schinagl.nl>

ARG TARGET_VERSION="3-alpine"
ARG TARGET_ARCH="library"

FROM docker.io/${TARGET_ARCH}/python:${TARGET_VERSION}

WORKDIR /usr/local/app

COPY . /usr/local/app

RUN _venv_dir="$(mktemp -d -p "${TMPDIR:-/tmp}" '_venv.XXXXXX')" && \
    python -m 'venv' "${_venv_dir}" && \
    "${_venv_dir}/bin/pip" install \
                                   'build' \
                                   'setuptools' \
                                   'wheel' \
    && \
    "${_venv_dir}/bin/python" -m build --wheel --no-isolation && \
    pip install './dist/yamllint-'*'.whl' && \
    rm -f -r "${_venv_dir}" && \
    rm -f -r "/usr/local/app"

COPY "./container-entrypoint.sh" "/init"

WORKDIR /usr/local/bin

ENTRYPOINT [ "/init" ]
