FROM python:alpine3.18

ENV USERNAME="versiondb"

RUN mkdir /app
WORKDIR /app
COPY src/requirements.txt /app/requirements.txt

RUN apk add --update tini bash curl && \
    apk add --update --virtual .build-deps gcc linux-headers musl-dev bash libffi-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    adduser -D ${USERNAME} && \
    chown ${USERNAME} -R /app /usr/local/bin /usr/local/lib/python3.*/site-packages && \
    find /usr/local \( -type d -a -name test -o -name tests \) \
        -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
        -exec rm -rf '{}' + && \
    apk del build-base && \
    rm -rf /var/cache/apk/* /root/.cache/pip

COPY src /app/

USER ${USERNAME}

EXPOSE 5001
ENV SHELL /bin/bash

ENTRYPOINT ["/sbin/tini", "--"]
CMD [ "/app/runme.sh" ]
