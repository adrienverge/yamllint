FROM python:3.5-alpine3.8

WORKDIR /yamllint
COPY . .

RUN python setup.py install

WORKDIR /

ENTRYPOINT [ "yamllint" ]
