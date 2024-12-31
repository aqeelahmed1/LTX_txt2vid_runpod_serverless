FROM runpod/pytorch:2.2.1-py3.10-cuda12.1.1-devel-ubuntu22.04

COPY builder/requirements.txt /requirements.txt
RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install  --upgrade pip && \
    python -m pip install --default-timeout=100 --upgrade -r /requirements.txt --no-cache-dir && \
    rm /requirements.txt

# NOTE: The base image comes with multiple Python versions pre-installed.
#       It is reccommended to specify the version of Python when running your code.


# Add src files (Worker Template)
ADD src .

RUN --mount=type=cache,target=/root/.cache/pip python3.9 /handler.py --default-timeout=100

CMD python -u /handler.py
