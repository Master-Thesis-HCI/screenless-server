FROM python:3.7

COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -U -r requirements.txt
COPY . /app

CMD ["python", "-u", "run.py"]
