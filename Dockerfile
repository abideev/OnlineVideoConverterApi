FROM nvidia/cuda:8.0-runtime-centos7

RUN  yum install -y \
  install centos-release-scl \
  epel-release \
  http://li.nux.ro/download/nux/dextop/el7/x86_64/nux-dextop-release-0-5.el7.nux.noarch.rpm

RUN yum update -y \
  && yum install -y \
  rh-python38 \
  rh-python38-python-pip \
  rh-python38-python-devel \
  ffmpeg \
  ffmpeg-compat \
  ffmpeg-compat-devel \
  ffmpeg-devel \
  ffmpeg-libs \
  && yum clean all

RUN mkdir -p /app/sources
RUN mkdir -p /app/data
RUN mkdir -p /download

WORKDIR /app

COPY sources /app/sources

RUN /opt/rh/rh-python38/root/usr/bin/pip3 install -r /app/sources/requirements.txt

