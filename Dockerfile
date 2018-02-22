FROM registry.esav.fi/base/python3

MAINTAINER Esa Varemo <esa@kuivanto.fi>

EXPOSE 6544

WORKDIR /

# Download the app

RUN useradd lsvtekniikka

RUN mkdir tilaushallinta && chown lsvtekniikka:lsvtekniikka tilaushallinta

USER lsvtekniikka
RUN git clone https://github.com/varesa/tilaushallinta.git tilaushallinta


# Install the app

WORKDIR /tilaushallinta/

USER root
RUN pip3.6 install --allow-external mysql-connector-python -e .


# Run

USER lsvtekniikka
CMD ["pserve", "development_mysql.ini"]

VOLUME /tilaushallinta/config
VOLUME /tilaushallinta/extfiles
