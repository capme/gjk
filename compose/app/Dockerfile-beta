FROM python:3.6

RUN apt-get update && apt-get install -y python-dev libxml2-dev libxslt1-dev zlib1g-dev vim \
    less build-essential git openssh-client supervisor libssl-dev libffi-dev && \
    apt-get clean && \
    mkdir -p /var/log/supervisor

COPY ./requirements.txt /requirements.txt

RUN pip install pip --upgrade \
  && pip install -r /requirements.txt --no-cache-dir

COPY ./compose/app/start.sh /start.sh
RUN chmod +x /start.sh

COPY ./compose/app/supervisord.conf /etc/supervisord.conf

WORKDIR /app

CMD ["/start.sh"]
