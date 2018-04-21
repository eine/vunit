#FROM python:alpine

COPY docker-bin /usr/local/bin/docker

RUN apk add --update curl bash \
  && rm -rf /var/cache/apk/* \
  && chmod +x /usr/local/bin/docker \
  && pip install colorama docker
