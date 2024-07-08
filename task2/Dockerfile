FROM python:3.9.17-bookworm

ENV PYTHONUNBUFFERED True

ENV APP_HOME /home/HNG/task2/

WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn -b :8080 api.v1.app:app