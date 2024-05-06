FROM python:3.12-bookworm

COPY entrypoint.py /entrypoint.py

RUN pip install git+https://github.com/AllSpiceIO/py-allspice.git

ENTRYPOINT [ "/entrypoint.py" ]
