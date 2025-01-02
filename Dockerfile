FROM runpod/pytorch:2.2.1-py3.10-cuda12.1.1-devel-ubuntu22.04

# FROM runpod/base:0.6.2-cuda12.6.2
# COPY builder/requirements.txt /requirements.txt
# RUN --mount=type=cache,target=/root/.cache/pip \
#     python -m pip install  --upgrade pip && \
#     python -m pip install --default-timeout=100 --upgrade -r /requirements.txt --no-cache-dir && \
#     rm /requirements.txt

RUN pip install -q torch==2.4.0+cu121 torchvision==0.19.0+cu121 torchaudio==2.4.0+cu121 torchtext==0.18.0 torchdata==0.8.0 --extra-index-url https://download.pytorch.org/whl/cu121 \
    tqdm==4.66.5 numpy==1.26.3 imageio==2.35.1 imageio-ffmpeg==0.5.1 xformers==0.0.27.post2 diffusers==0.30.3 moviepy==1.0.3 transformers==4.44.2 accelerate==0.33.0 sentencepiece==0.2.0 pillow==9.5.0 runpod
RUN pip install git+https://github.com/huggingface/diffusers
# NOTE: The base image comes with multiple Python versions pre-installed.
#       It is reccommended to specify the version of Python when running your code.


# Add src files (Worker Template)
ADD src .

RUN --mount=type=cache,target=/root/.cache/pip python /handler.py --default-timeout=100

CMD python -u /handler.py
