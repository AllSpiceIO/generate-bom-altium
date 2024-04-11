FROM python:3.12-bookworm

COPY entrypoint.py /entrypoint.py

RUN pip install py-allspice

ENTRYPOINT [ "/entrypoint.py" ]
