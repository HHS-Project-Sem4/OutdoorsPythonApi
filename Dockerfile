## Choose our version of Python
#FROM python:3.9
#
#RUN apt-get install g++
#
## Install unixodbc-dev
#RUN apt-get update && apt-get install -y unixodbc-dev
#
#RUN apt-get update
#
## Install msodbcsql17
#RUN apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17
#
#
## Set up a working directory
#WORKDIR /code
#
## Copy just the requirements into the working directory so it gets cached by itself
#COPY ./requirements.txt /code/requirements.txt
#
## Install the dependencies from the requirements file
#RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
#
## Copy the code into the working directory
#COPY ./app /code/app
#
## Tell uvicorn to start spin up our code, which will be running inside the container now
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
#


# Base image
FROM python:3.9-slim

# Install ODBC Driver 17 for SQL Server
RUN apt-get update && apt-get install -y gnupg2 curl && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Set working directory
WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port that the FastAPI app will listen on
EXPOSE 8000

# Tell uvicorn to start spin up our code, which will be running inside the container now
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]