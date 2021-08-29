FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN mkdir -p /app
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
CMD PYTHONPATH=/app python main.py
