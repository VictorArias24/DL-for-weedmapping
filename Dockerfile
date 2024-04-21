# Base image with Python 3.10 and PyTorch 2.1.0
FROM runpod/pytorch:2.1.0-py3.10-cuda11.8.0-devel-ubuntu22.04

# internal port
EXPOSE 8080

ENTRYPOINT ["/bin/bash"]

# Update the list of available packages
RUN apt update

# Install git and wget using apt package manager
RUN apt install git wget -y

# Install runpod, a library for serverless computing
RUN pip install datasets

# Set the working directory to '/workspace/app'
WORKDIR /app