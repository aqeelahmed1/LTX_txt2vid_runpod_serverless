# FROM nvidia/cuda:12.0.0-cudnn8-devel-ubuntu22.04
# SHELL ["/bin/bash", "-o", "pipefail", "-c"]
ARG BASE_IMAGE=nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04
FROM ${BASE_IMAGE} as dev-base


SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN apt-key del 7fa2af80
RUN apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/3bf863cc.pub
RUN apt-get update --yes && \
    apt-get upgrade --yes && \
    apt install --yes --no-install-recommends\
    wget\
    bash\
    openssh-server \
    software-properties-common &&\
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get install python3.10 python3-pip -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen



# Python dependencies
COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python3.10 -m pip install  --upgrade pip && \
    python3.10 -m pip install --default-timeout=100 --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# NOTE: The base image comes with multiple Python versions pre-installed.
#       It is reccommended to specify the version of Python when running your code.


# Add src files (Worker Template)
ADD src .

RUN --mount=type=cache,target=/root/.cache/pip python3.10 /handler.py --default-timeout=100

CMD python3.10 -u /handler.py
