FROM python:3
ADD . /yamllint

RUN pip install /yamllint

WORKDIR /yamllint
CMD yamllint
