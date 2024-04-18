FROM python:3.9.13-slim

COPY requirements.txt requirements.txt
RUN pip install -U pip && pip install -r requirements.txt

COPY ./api /app/api
COPY ./bin /app/bin
COPY ./lingo /app/lingo
COPY ./spec /app/spec
COPY ./templates /app/templates
COPY wsgi.py /app/wsgi.py
COPY config.py /app/config.py
COPY server.py /app/server.py
COPY ./utils /app/utils
COPY lingoServiceAccountKey.json /app/lingoServiceAccountKey.json

WORKDIR /app

RUN useradd lingo
USER lingo

EXPOSE 8000

ENTRYPOINT ["bash", "/app/bin/run.sh"]