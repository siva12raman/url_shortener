FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=5001

# Set working directory
WORKDIR /app

# Copy dependency definition and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source files
COPY . .

# Expose application port
EXPOSE 5001

# Run Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "app:app"]
