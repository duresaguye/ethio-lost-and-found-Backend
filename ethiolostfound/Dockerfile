# Use a Python image
FROM python:3.10-slim

WORKDIR /app

COPY . /app

# Install dependencies with a faster mirror and increased timeout
RUN pip install --no-cache-dir --index-url https://pypi.org/simple --timeout=600 -r requirements.txt



# Command to start your Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
