FROM    python:3-alpine

RUN     pip install --upgrade Flask gunicorn prometheus_client requests pyyaml

ENV     PORT=9898
ENV     APP_HOME=/app
WORKDIR $APP_HOME
COPY    *.py $APP_HOME

CMD     exec gunicorn --bind ":$PORT" --workers 1 --threads 1 homewizard-apiv2-exporter:app
