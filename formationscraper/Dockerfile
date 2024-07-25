FROM mcr.microsoft.com/azure-functions/python:4-python3.10

ENV host:logger:consoleLoggingMode=always

COPY . /home/site/wwwroot
COPY ./requirements.txt /home/site/wwwroot

RUN cd /home/site/wwwroot && pip install -r requirements.txt