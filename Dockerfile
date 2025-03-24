# Use Python 3.10 slim image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev vim && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Set permissions for the SDK and install SDK libraries
RUN chmod -R +x /usr/src/app/sdk/setup && cd /usr/src/app/sdk/setup && ./install

# Copy the libraries from SDK to /usr/lib64/
COPY sdk/setup/sdk-porting-linux-rpi/opt/DigitalPersona/UareUSDK/Linux/lib/x64/ /usr/lib64/

# Ensure correct permissions
RUN chmod -R 777 /usr/src/app/media

# Expose port 8000
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "api_finger_print.wsgi:application"]