FROM python:3.8-alpine

# Set up a working directory
WORKDIR /code

# Copy just the requirements into the working directory so it gets cached by itself
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies from the requirements file
RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    build-base \
    libressl-dev \
    libffi-dev \
    && pip install --no-cache-dir --upgrade -r /code/requirements.txt \
    && apk del .build-deps

# Copy the code into the working directory
COPY ./app /code/app

# Tell uvicorn to start spin up our code, which will be running inside the container now
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
