FROM python:3.12.3-slim-bullseye

RUN apt-get update
RUN apt-get install -y curl vim net-tools

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt

EXPOSE 8001

CMD ["python", "init.py"]

