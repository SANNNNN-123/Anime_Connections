# Use Python 3.12 Bullseye as the base image
FROM python:3.12-bullseye

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Use PORT environment variable
ENV PORT=8000

# Expose port
EXPOSE $PORT

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
