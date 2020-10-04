# libmariadb3 on debian is too old, see https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=962597
FROM python:3.8-alpine

MAINTAINER Esa Varemo <esa@kuivanto.fi>

EXPOSE 6544

WORKDIR /

ADD . /tilaushallinta
WORKDIR /tilaushallinta

RUN addgroup -S tilausapp && \
    adduser -G tilausapp -S tilausapp && \
    chown tilausapp:tilausapp /tilaushallinta && \
    apk add gcc python3-dev libffi-dev musl-dev mariadb-dev mariadb-connector-c && \
    pip install -e .

USER tilausapp
CMD ["pserve", "development_mysql.ini"]

VOLUME /tilaushallinta/config
VOLUME /tilaushallinta/extfiles
