FROM python:3.10-slim-buster

RUN apt update
RUN apt install -y libpq-dev cron g++ build-essential

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./server .

COPY ./entrypoint.sh /
RUN chmod u+x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]