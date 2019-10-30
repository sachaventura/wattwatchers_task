FROM python:3

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app

RUN python3 unit_tests.py

CMD [ "python3", "app.py" ]