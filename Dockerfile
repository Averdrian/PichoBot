FROM debian:stable-slim

RUN apt update
RUN apt install python3 git -y

ENTRYPOINT ["python3"]