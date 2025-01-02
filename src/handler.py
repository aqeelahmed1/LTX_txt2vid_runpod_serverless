""" Example handler file. """
print('************* loading imports *************')

from PIL import Image
import runpod

import torch
from diffusers import LTXPipeline
from diffusers import LTXImageToVideoPipeline

from diffusers.utils import export_to_video
from utils import *
import time

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")


print('************* loading pipeline *************',device)

pipe = LTXPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)
pipe.to("cuda")
pipe_im2vid = LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video", torch_dtype=torch.bfloat16)
pipe_im2vid.to("cuda")

print('************* loaded pipeline *************')


def handler(job):
    """ Handler function that will be used to process jobs. """
    print('==start===')

    if device!='cpu':
        time_start = time.time()
        job_input = job['input']
        print(job_input)
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
            print('======== img to vid =============')
            image_bytes = base64.b64decode(image_base64)
            # Convert the bytes to an image
            image = Image.open(BytesIO(image_bytes))
            video = pipe_im2vid(
                image=image,
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_frames=num_frames,
                num_inference_steps=num_inference_steps,
            ).frames[0]

        else:
            print('=========txt to vid===============')
            video = pipe(
                prompt=prompt,
                negative_prompt=negative_prompt,
                width=width,
                height=height,
                num_frames=num_frames,
                num_inference_steps=num_inference_steps,
            ).frames[0]
        # export_to_video(video, "output.mp4", fps=24)
        print('finshed generating')

        file_name = "new_out.mp4"
        export_to_video(video, file_name, fps=fps)

        print("time elapsed:", time.time() - time_start)
        encoded_frames=encode_video_to_base64(file_name)
        return encoded_frames

    else:
        print("No GPU found")
        return {"device",device}

    # except:
    #     return {'Comment':'Error Occured'}


runpod.serverless.start({"handler": handler})
