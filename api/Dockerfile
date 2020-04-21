############ Build ########################
FROM python:3.7-alpine3.10 as build

COPY requirements.txt .
RUN apk add --update --no-cache linux-headers g++ libffi-dev libxslt-dev libressl-dev make python3-dev \
    && pip wheel --wheel-dir=/root/wheels -r requirements.txt

############ Release ######################
FROM python:3.7-alpine3.10 as release

ENV TZ UTC
COPY --from=build /root/wheels /root/wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/root/wheels -r requirements.txt && \
    apk add --no-cache libressl2.7-libssl libxml2 libxslt curl tzdata libuuid
COPY app app
COPY boot.sh config.py run.py ./
RUN chmod +x boot.sh

############ Security Checks ##############
ADD https://get.aquasec.com/microscanner .
RUN chmod +x microscanner && \
    ./microscanner MWE5NDhlZjk2OTJm && \
    rm microscanner
RUN pip install safety
RUN safety check
RUN pip uninstall -y safety

############ Run Application ##############
RUN addgroup -g 9001 appgroup && adduser -u 9001 -S appuser -G appgroup
USER appuser
ENV TZ UTC
ENTRYPOINT ["./boot.sh"]
HEALTHCHECK CMD curl --fail http://localhost:5000/ || exit 1
LABEL autoheal=true