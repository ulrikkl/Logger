FROM python:slim

RUN useradd logger

WORKDIR /home/logger

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY migrations migrations
COPY logger.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP logger.py
ENV SETUP_STATUS 0

RUN chown -R logger:logger ./
USER logger

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]