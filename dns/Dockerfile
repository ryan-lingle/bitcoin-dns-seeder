FROM python:3.6

EXPOSE 53/tcp
EXPOSE 53/udp

WORKDIR /dns

COPY . /dns

RUN pip install -r requirements.txt

CMD python dnserver.py

