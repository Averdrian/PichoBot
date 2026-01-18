FROM debian:stable-slim

RUN apt update
RUN apt install python3 python3-pip git -y

RUN git clone https://github.com/Averdrian/PichoBot
WORKDIR /PichoBot
COPY .env /PichoBot/.env

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt

ENTRYPOINT ["python3", "app.py"]