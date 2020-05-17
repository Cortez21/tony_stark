FROM python:3.8

RUN mkdir -p /urs/src/app
WORKDIR /urs/src/app

COPY . /urs/src/app

#RUN apt-get update | apt-get install python3-pip
RUN pip install -r requirements.txt

EXPOSE 5432

CMD ["python3", "launch.py"]