FROM python:3.9.20-slim-bullseye
RUN mkdir /app
COPY ./app /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN  pip install --upgrade pip setuptools wheel \
    && pip install -r requirements.txt\
    && rm -rf /root/.cache/pip
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]