FROM ubuntu:18.04
LABEL maintainer="Suravi Mandal <survimails@gmail.com>"
RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx gcc musl-dev libpq-dev python3-dev postgresql-server-dev-all
RUN pip3 install uwsgi psycopg2-binary
COPY . .
WORKDIR .
RUN pip3 install -r requirements.txt

CMD [ "python3", "app.py" ]

