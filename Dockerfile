FROM python:3.13.2

WORKDIR /app

COPY main.py /app/
COPY utils.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt
CMD ["python", "main.py"]

