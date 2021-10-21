FROM python:3.8.7-slim


COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY ./notibara /notibara


CMD ["python", "-m", "notibara"]