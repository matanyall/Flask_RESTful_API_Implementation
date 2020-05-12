FROM python:3.6

ADD . /pyarcade

ADD wait-for-it.sh /usr/bin/

RUN chmod u+x /usr/bin/wait-for-it.sh

WORKDIR /pyarcade

RUN pip install -r requirements.txt && \
    pip install .
