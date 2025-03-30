FROM python:3.13

WORKDIR /code
RUN apt-get update && apt-get install -y sqlite3
COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/

CMD ["fastapi", "dev", "api.py", "--port", "8000", "--host", "0.0.0.0", "--reload"]
