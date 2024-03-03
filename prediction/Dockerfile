FROM python:3.8

# Set the working directory within the container
WORKDIR /app

# Copy the necessary files and directories into the container
COPY requirements.txt /app
COPY .env /app
COPY app.py /app
COPY settings.yaml /app
COPY static/ /app/static/
COPY storage/ /app/storage/
COPY templates/ /app/templates/

# Upgrade pip and install Python dependencies
RUN pip3 install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask application
EXPOSE 5000

CMD ["export","ENVIRONMENT=${ENVIRONMENT}"]
# Define the command to run the Flask application using Gunicorn
CMD ["python3", "app.py"]
