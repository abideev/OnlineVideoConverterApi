FROM nvidia/cuda:11.0-base-centos7

RUN yum update -y && yum upgrade -y && yum install -y ffmpeg

RUN mkdir /app

COPY sources /app

WORKDIR /app
ENTRYPOINT ["/usr/bin/ffmpeg"]
CMD ["-h"]