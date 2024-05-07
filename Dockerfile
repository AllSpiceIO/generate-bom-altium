FROM python:3.12-bookworm

COPY entrypoint.py /entrypoint.py

RUN pip install git+https://github.com/AllSpiceIO/py-allspice.git@1aaecf72f35dec1310e8bf0fb5cac19df11ffe94

ENTRYPOINT [ "/entrypoint.py" ]
