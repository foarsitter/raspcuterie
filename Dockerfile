FROM debian:buster

RUN apt-get update && apt-get --assume-yes install python3-pip

COPY ./requirements.txt /requirements.txt
COPY . /app

RUN pip3 install -r /requirements.txt



WORKDIR /app

CMD ["flask", "run" ,"0.0.0.0"]