FROM python:3.13.1-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["fastapi", "run", "main.py"]
