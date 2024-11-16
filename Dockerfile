FROM python:3.9-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copy application files
COPY chocolate-house-app.py .

RUN mkdir templates
COPY templates/index.html templates/

# Create directory for SQLite database and set permissions
RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Set environment variable for Flask
ENV FLASK_APP=chocolate-house-app.py
ENV FLASK_ENV=development
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "chocolate-house-app.py"]