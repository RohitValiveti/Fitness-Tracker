FROM python:3.9.12

RUN mkdir server
WORKDIR server

COPY . .

RUN pip3 install -r requirements.txt

CMD python3 app.py