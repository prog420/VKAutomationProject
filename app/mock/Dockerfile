FROM python:3.8-slim

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

CMD [ "python", "/app/app.py" ]

# docker build -t flask-app .
# docker run --name flapp -it -p 8083:8083 -d flask-app
# docker exec -it flapp /bin/sh