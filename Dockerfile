FROM python:3.9-alpine
LABEL maintainer="Jope Algorta"

ENV PYTHONUNBUFFERED 1
ENV PATH="/scripts:$PATH"

COPY ./requirements.txt /requirements.txt
COPY ./scripts /scripts
RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc python3-dev linux-headers build-base postgresql-dev musl-dev zlib-dev libjpeg
RUN pip install --upgrade pip && pip install -r /requirements.txt
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app
EXPOSE 8000

RUN mkdir -p /vol/web/media && mkdir -p /vol/web/static
RUN adduser -D user
RUN chown -R user:user /vol/ && chmod -R 755 /vol/web && chmod -R +x /scripts
USER user

CMD ["sh"]
