FROM alpine

COPY requirements.txt /tmp/requirements.txt

RUN apk add --no-cache \
    libc6-compat \
    alpine-sdk \
    python3-dev \
    py-pip \
    linux-headers \
    python3 \
    git &&\
    pip3 install --upgrade pip setuptools && \
    pip3 install six && \
    pip3 install mock && \
    pip3 install -r /tmp/requirements.txt


RUN mkdir -p /var/log/app/
RUN chmod 777 -R /var/log/app/

COPY . /app
WORKDIR /app

ENV FLASK_APP=app.py

RUN chmod 777 ./start.sh

CMD ["ash", "-c", "./start.sh"]
