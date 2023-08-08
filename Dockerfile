FROM python:latest as base

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y locales locales-all && \
    rm -rf /var/cache/apt/archives /var/lib/apt/lists/*.

ENV LANG="de_DE.UTF-8" \
    LANGUAGE="de_DE.UTF-8" \
    LC_ALL="de_DE.UTF-8" \
    TZ=Europe/Berlin

STOPSIGNAL SIGINT

FROM base as builder

COPY requirements.txt /requirements.txt

RUN python --version && \
    pip --version && \
    pip install --prefix=/install -r requirements.txt

FROM base

LABEL   org.opencontainers.image.description="Feiertagsbot für Slack benachrichtigt über im definierten Zeitraum über bevorstehende Feiertage in deutschen Bundesländern" \
        org.opencontainers.image.authors="Kim Oliver Drechsel <kim@drechsel.xyz>" \
        org.opencontainers.image.licenses="MIT"

ENV SEARCH_WEEKS=2 \
    STATE=ALL

WORKDIR /app/
COPY --from=builder /install /usr/local
COPY main.py .

USER 1000

CMD ["python3", "main.py"]
