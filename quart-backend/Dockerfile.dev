FROM python:3.11-slim
ENV PYTHONUNBUFFERED=1
# Set working directory
WORKDIR /app

# Copy files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port
EXPOSE 8000

# Run app
CMD ["python", "reload_watcher.py"]