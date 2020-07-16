FROM python:3.7
WORKDIR /usr/src/
COPY ./requirements.txt ./requirements.txt
RUN pip install -r requirements.txt && pip install gunicorn && apt-get clean
COPY ./ ./
RUN chmod +x /usr/src/boot_flask.sh
