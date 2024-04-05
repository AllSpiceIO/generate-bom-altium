FROM ubuntu:latest

COPY entrypoint.py /entrypoint.py

RUN pip install py-allspice

ENTRYPOINT [ "/entrypoint.py" ]