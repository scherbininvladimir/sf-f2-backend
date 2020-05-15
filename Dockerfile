FROM python:3.7.6
WORKDIR /app
COPY ./requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install gunicorn
