FROM python:3.7

ENV POETRY_VERSION=1.1.3 \
    POETRY_VIRTUALENVS_IN_PROJECT=true
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=$PATH:/root/.poetry/bin

ARG CHROME_VERSION="google-chrome-stable"
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update -y \
  && apt-get install -y \
    ${CHROME_VERSION:-google-chrome-stable} \
  && rm /etc/apt/sources.list.d/google-chrome.list \
  && rm -rf /var/lib/apt/lists/* /var/cache/apt/*
# https://github.com/SeleniumHQ/docker-selenium/blob/d701fd422b6418c30209dcf7442fd0c51791d585/NodeChrome/wrap_chrome_binary
RUN curl https://raw.githubusercontent.com/SeleniumHQ/docker-selenium/d701fd422b6418c30209dcf7442fd0c51791d585/NodeChrome/wrap_chrome_binary | bash

WORKDIR /dcbot
ENV PATH=/dcbot/.venv/bin:$PATH
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-dev --no-root
COPY dcbot ./dcbot
RUN poetry install --no-dev

WORKDIR /workspace

CMD dcbot --help
