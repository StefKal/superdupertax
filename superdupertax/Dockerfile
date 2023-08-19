FROM python:3.10-bullseye

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apt-get update

# create directory for the app user
RUN addgroup --system appgroup && \
    adduser --system appuser --ingroup appgroup && \
    mkdir -p /home/superdupertax/web && \
    chown -R appuser:appgroup /home/superdupertax

RUN python -m pip install --upgrade pip setuptools wheel

COPY ./requirements.txt .

RUN pip install --no-deps -r requirements.txt

# change to the app user
USER appuser

# set work directory
WORKDIR /home/superdupertax/web

# copy project
COPY --chown=appuser:appgroup . /home/superduperapp/web

# run entrypoint.sh
CMD ["bash", "/home/superdupertax/web/entrypoint.sh"]
