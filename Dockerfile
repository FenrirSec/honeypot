FROM python:3.8-buster

WORKDIR /app

COPY ./protocols /app/protocols
COPY ./templates /app/templates
COPY main.py logger.py faker.py requirements.txt /app/

RUN ls -lah /app
RUN mkdir /app/logs && mkdir /app/keys && ssh-keygen -f /app/keys/ssh_host_rsa_key
RUN pip install -r requirements.txt

CMD ["python3", "main.py"]