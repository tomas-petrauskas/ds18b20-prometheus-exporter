# Use the official Python image as a base
FROM python:3.11-slim

# Create and set the working directory
WORKDIR /app

# Copy the application files into the container
COPY requirements.txt /app/
COPY main.py /app/

# Install the required Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Prometheus will scrape (default: 8000)
EXPOSE 80

# Set the entry point to run the script
CMD ["python", "main.py"]