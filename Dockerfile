FROM python:3.6
LABEL maintainer="Suravi Mandal <survimails@gmail.com>"
RUN apt-get update
COPY . .
WORKDIR .
RUN pip3 install --no-cache-dir -r requirements.txt
ENV FLASK_ENV='production'
CMD flask run