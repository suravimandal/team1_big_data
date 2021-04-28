FROM python:3.6
LABEL maintainer="Suravi Mandal <survimails@gmail.com>"
RUN apt-get update
COPY . .
WORKDIR .
RUN python3.6 -m pip install --no-cache-dir -r requirements.txt
ENV FLASK_ENV='production'
EXPOSE 5000
CMD python3 app.py
