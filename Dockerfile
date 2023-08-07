FROM python:3.8

WORKDIR /webapps

COPY . /webapps

RUN pip --no-cache-dir install --upgrade pip setuptools
RUN pip --no-cache-dir install -r requirements.txt
RUN pip --no-cache-dir install -r lib/requirements.txt
RUN pip --no-cache-dir install "Flask[async]"
