FROM python:3.11

# Set the working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/tadiyusss/very-secure-bank .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV DJANGO_DEBUG=${DJANGO_DEBUG}
ENV DJANGO_ALLOWED_HOSTS=${DJANGO_ALLOWED_HOSTS}

# Expose the application's port
EXPOSE 8000

# Run Django migrations and start the server
CMD python manage.py makemigrations very_secure_bank && python manage.py migrate && python manage.py runserver 0.0.0.0:8000
