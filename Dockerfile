FROM python:3-alpine3.10

WORKDIR /
COPY . /src
RUN pip install --no-cache-dir /src && \
    rm -rf ~/.cache/pip && \
    rm -rf /src

ENTRYPOINT [ "yamllint" ]
CMD ["--version"]
