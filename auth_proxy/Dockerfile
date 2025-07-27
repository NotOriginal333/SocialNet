FROM python:3.12-alpine3.22

ENV PYTHONUNBUFFERED=1

WORKDIR /auth_proxy

COPY requirements.txt /tmp/requirements.txt
COPY . .

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

EXPOSE 5000

ENV PATH="/py/bin:$PATH"

CMD ["flask", "run"]