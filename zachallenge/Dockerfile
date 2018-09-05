FROM ubuntu:latest

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip
###########################################################
RUN apt-get --assume-yes install ffmpeg
RUN mkdir -p /model
WORKDIR /model
COPY requirements.txt /model/requirements.txt
RUN pip3 install -r requirements.txt
# RUN apt-get install systemd-services
# RUN timedatectl set-timezone Asia/Ho_Chi_Minh
# RUN apt-get --assume-yes install python3-tk
COPY . /model
RUN chmod 755 /model/predict.sh
ENV PYTHONPATH=/model:$PYTHONPATH
ENTRYPOINT ["/bin/sh"]
# CMD /model/predict.sh
