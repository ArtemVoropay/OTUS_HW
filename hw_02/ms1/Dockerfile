FROM python:3.9.20-slim-bullseye
RUN mkdir /app
COPY ./main.py /app
WORKDIR /app/
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]