FROM python:3.7.5
ENV PYTHONUNBUFFERED 1

RUN mkdir -p /usdc/code
WORKDIR /usdc/code

RUN mkdir /usdc/mediafiles
RUN mkdir /usdc/staticfiles
RUN mkdir /usdc/logs

COPY requirements.txt /usdc/code/
RUN pip install -r requirements.txt

ADD . /usdc/code/

# RUN chmod +x ./gunicorn_run