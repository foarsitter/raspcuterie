FROM debian:buster-slim

RUN apt-get update && apt-get --assume-yes install python3-pip

COPY ./requirements.txt /requirements.txt
COPY . /app
COPY ./config_dev.yaml /root/.config/raspcuterie/config.yaml

RUN pip3 install -r /requirements.txt

RUN pip3 install /app
RUN which raspcuterie

WORKDIR /app

ENV FLASK_APP=raspcuterie.app

CMD ["flask", "run" ,"-h", "0.0.0.0"]