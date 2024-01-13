FROM python:3.10-alpine
WORKDIR /code1
COPY requirements1.txt /code1
RUN pip install -r requirements1.txt --no-cache-dir
COPY ./code1 /code1
CMD ["python", "/code1/app.py"]