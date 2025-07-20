FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8000", "--reload"]