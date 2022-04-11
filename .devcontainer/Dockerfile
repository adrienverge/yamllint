# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.224.3/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10-bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# CA Certificate using a script that read the files from the ./certs directory
#COPY certs/. /usr/local/share/ca-certificates/
#ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/my_company.pem
#RUN sudo update-ca-certificates

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] Add Tini, it operates as a process subreaper for jupyter. This prevents kernel crashes.
# Load before `requirements.txt`, probably more stable in that order
# This allows VSCode to open notebook files and run them from within the IDE (this does NOT support in a Browser use)
ENV TINI_VERSION v0.6.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini
ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# original files from the project
# none

# added for devcontainer convenience
COPY requirements_dev.txt /tmp/pip-tmp/
RUN pip3 --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --disable-pip-version-check \
    --no-cache-dir \
    install -r /tmp/pip-tmp/requirements_dev.txt

COPY requirements_user.txt /tmp/pip-tmp/
RUN pip3 --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --disable-pip-version-check \
    --no-cache-dir \
    install -r /tmp/pip-tmp/requirements_user.txt

RUN rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
# RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#     && apt-get -y install --no-install-recommends <your-package-list-here>

# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1

# [Optional] Uncomment this line to install sqlite.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends sqlite3
