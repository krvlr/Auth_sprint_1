FROM python:3.10
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src .
ENTRYPOINT gunicorn --worker-class gevent --workers 1 --bind 0.0.0.0:8000 main:app