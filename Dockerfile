FROM nvidia/cuda:11.2.2-cudnn8-runtime-ubuntu20.04

# Set environment variable to avoid timezone configuration prompt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.9, pip, ffmpeg, and git
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3.9 \
    python3.9-distutils \
    python3-pip \
    libsndfile1 \
    ffmpeg \
    git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure the timezone (set to UTC)
RUN ln -fs /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    dpkg-reconfigure --frontend noninteractive tzdata

# # Set the working directory to /app
# WORKDIR /app
#
# # Add app files (Worker Template)
# COPY app /app

# Update alternatives to use Python 3.9
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Set LD_LIBRARY_PATH environment variable
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib/python3.9/dist-packages/nvidia/cudnn/lib


# Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python3.9 -m pip install  --upgrade pip && \
    python3.9 -m pip install --default-timeout=100 --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# NOTE: The base image comes with multiple Python versions pre-installed.
#       It is reccommended to specify the version of Python when running your code.


# Add src files (Worker Template)
ADD src .

RUN --mount=type=cache,target=/root/.cache/pip python3.9 /handler.py --default-timeout=100

CMD python3.9 -u /handler.py
