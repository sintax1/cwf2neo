FROM python:3.7

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app.py wait-for-it.sh ./

CMD ["python", "app.py"]