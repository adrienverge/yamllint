# Dockerfile to run the test suite and linter
FROM python:slim
RUN pip install flake8 flake8-import-order doc8 yamllint \
 && apt-get update \
 && apt-get install -y locales \
 && rm -rf /var/lib/apt/lists/* \
 && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
