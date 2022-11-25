FROM python:3.10.6-alpine

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . /usr/src/app/

RUN pip install -r requirements.txt --compile --no-cache-dir
CMD ["python3", "app.py"] 