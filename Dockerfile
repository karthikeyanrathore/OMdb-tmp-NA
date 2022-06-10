FROM python:3.8-slim-buster

LABEL maintainer="Karthikeyan rathore <karthikeyan@fasal2022>"

WORKDIR /home/fasal

COPY requirements.txt /home/fasal/requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["./run.sh"]


