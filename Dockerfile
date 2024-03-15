# Use the official Python image as the base image
FROM python:3.12.2

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the current directory contents into the container at /app
COPY . /app

# Expose the port your app runs on
EXPOSE 8000

# Define the command to run your app using gunicorn
# Adjust the command according to your application's needs
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "kjjinn.wsgi:application"]
