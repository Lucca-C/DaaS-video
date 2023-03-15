FROM python:3

RUN mkdir -p /home/daas-video
WORKDIR /home/daas-video

RUN pip install --upgrade pip

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD app app
ADD boot.sh ./
RUN chmod +x boot.sh

RUN mkdir data
ADD ./data/26171_xaif.json ./data/26171_xaif.json

ENV FLASK_APP app


EXPOSE 5000
ENTRYPOINT ["./boot.sh"]