FROM python:3.12

ENV PYTHONUNBUFFERED 1

WORKDIR /payment

COPY requirements.txt /payment/

RUN pip install -r requirements.txt

COPY . /payment/

RUN python manage.py migrate

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]