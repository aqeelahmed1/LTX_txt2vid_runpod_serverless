""" Example handler file. """
from PIL import Image
import runpod
import torch
from diffusers import LTXPipeline
from diffusers.utils import export_to_video
from utils import *
import time

try:
    pipe = LTXPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)
    pipe.to("cuda")

except RuntimeError:
    quit()


def handler(job):
    """ Handler function that will be used to process jobs. """

    time_start = time.time()
    job_input = job['input']
    image_base64 = job_input.get('image',None)
    prompt = job_input.get('prompt',None)
    negative_prompt=job_input.get('negative_prompt',None)
    width=job_input.get('width',704)
    height=job_input.get('height',480)
    num_frames=job_input.get('num_frames',161)
    num_inference_steps=job_input.get('num_inference_steps',32)
    fps=job_input.get('fps',24)

    MAX_HEIGHT = 720
    MAX_WIDTH = 1280
    MAX_NUM_FRAMES = 257

    height=min(height,MAX_HEIGHT)
    width=min(width,MAX_WIDTH)
    num_frames=min(num_frames,MAX_NUM_FRAMES)
    image=None
    if image_base64 is not None:
        image_bytes = base64.b64decode(image_base64)
        # Convert the bytes to an image
        image = Image.open(BytesIO(image_bytes))

    try:
        video = pipe(
            image=image,
            prompt=prompt,
            negative_prompt=negative_prompt,
            width=width,
            height=height,
            num_frames=num_frames,
            num_inference_steps=num_inference_steps,
        ).frames[0]
        # export_to_video(video, "output.mp4", fps=24)

        file_name = "new_out.mp4"
        export_to_video(video, file_name, fps=fps)

        print("time elapsed:", time.time() - time_start)
        encoded_frames=encode_video_to_base64(file_name)
        return encoded_frames
    except:
        return {'Comment':'Error Occured'}


runpod.serverless.start({"handler": handler})
