""" Example handler file. """
print('************* loading imports *************')

from PIL import Image
import runpod

import torch
# from diffusers import LTXPipeline
# from diffusers import LTXImageToVideoPipeline
#
# from diffusers.utils import export_to_video
# from utils import *
# import time

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print('************* loading pipeline *************', device)


print('************* loaded pipeline *************')


def handler(job):
    """ Handler function that will be used to process jobs. """
    print('==start===')

    print('************* device *************', device)

    print("No GPU found")
    return {"device", device}


runpod.serverless.start({"handler": handler})
