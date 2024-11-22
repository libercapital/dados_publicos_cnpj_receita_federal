# get base image
FROM python:3.8-slim

RUN apt-get update && apt-get install -y locales locales-all

WORKDIR /app

RUN mkdir -p /app/src/ \
    mkdir -p /app/tests/

ENV PYTHONPATH="${PYTHONPATH}:/app/:/root/.local/bin/"

COPY ./pytest.ini ./pytest.ini
COPY ./.coveragerc ./.coveragerc
COPY requirements/ requirements/

# install requirements/production.txt on docker image
RUN pip install --user --no-cache-dir -r requirements/requirements.txt \
    && find /root/.local/ -follow -type f -name '*.a' -name '*.txt' -name '*.md' -name '*.png' -name '*.jpg' \
                                           -name '*.jpeg' -name '*.js.map' -name '*.pyc' -name '*.c' -name '*.pxc' \
                                           -name '*.pyc' -delete \
    && find /usr/local/lib/python3.8 -name '__pycache__' | xargs rm -r
ENV LANG=C.UTF-8

COPY src/ src/
COPY tests/ tests/

CMD ["bash"]
