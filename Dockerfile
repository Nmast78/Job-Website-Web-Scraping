FROM nikolaik/python-nodejs:latest
# FROM python:3
# Set the working directory to /usr/src/app.
WORKDIR /usr/src/app
# Copy the file from the local host to the filesystem of the container at the working directory.
COPY requirements.txt ./
# Install Scrapy specified in requirements.txt.
RUN pip3 install --no-cache-dir -r requirements.txt
# Install playwright
RUN playwright install
# Install playwright dependencies
RUN playwright install-deps
# Install bs4
RUN pip3 install bs4
# Copy the project source code from the local host to the filesystem of the container at the working directory.
COPY . .