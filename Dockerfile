# Using official Python image
FROM python:3.11
LABEL authors="JxSol"

# Define variables
ARG APP_HOME=/app

# Set working directory inside the container
WORKDIR $APP_HOME

# Prohibit Python to creating cache files inside the container
ENV PYTHONDONTWRITEBYTECODE=1
# Prohibit buffer stdout
ENV PYTHONUNBUFFERED=1

# Update the system
RUN apt update && \
    apt install -y --no-install-recommends gcc

# Copy requirements files
COPY requirements.txt $APP_HOME/requirements.txt

# Install the requirements
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . $APP_HOME

CMD python manage.py collectstatic --noinput \
    && python manage.py makemigrations --noinput \
    && python manage.py migrate --noinput \
    && gunicorn config.wsgi:application --bind 0.0.0.0:8000