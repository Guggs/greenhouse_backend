FROM python:3.10

WORKDIR /code

ENV PYTHONPATH "${PYTHONPATH}:/code/greenhouse_api/app"

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "80"]