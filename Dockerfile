FROM python:3.12-bookworm

COPY entrypoint.py /entrypoint.py

RUN pip install git+https://github.com/AllSpiceIO/py-allspice.git@d3182f167c54c71e490c4ecd35bb4f4dfeabe913

ENTRYPOINT [ "/entrypoint.py" ]
