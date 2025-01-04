print("*********************** step 1***************************")
import os, json, requests, random, runpod
import torch
from diffusers import AutoencoderKLCogVideoX, CogVideoXImageToVideoPipeline, CogVideoXTransformer3DModel
from diffusers.utils import export_to_video, load_image
from transformers import T5EncoderModel, T5Tokenizer
import base64
from PIL import Image
from io import BytesIO


# Function to encode image into Base64
def encode_image_to_base64(image_path):
    # Open the image file
    with Image.open(image_path) as img:
        # Convert the image to byte array using BytesIO
        buffered = BytesIO()
        img.save(buffered, format="PNG")  # Save as PNG or other formats (e.g., JPG)
        img_byte_array = buffered.getvalue()

    # Encode the byte array to base64
    base64_string = base64.b64encode(img_byte_array).decode('utf-8')
    return base64_string


# Function to decode Base64 and save the image
def decode_base64_and_save(encoded_str, output_image_path):
    # Decode the Base64 string into bytes
    image_data = base64.b64decode(encoded_str)

    # Write the decoded data to a new image file
    with open(output_image_path, 'wb') as image_file:
        image_file.write(image_data)

    print(f"Image has been saved to {output_image_path}")


def encode_video_to_base64(video_file_path):
    """
    Encodes a video file to a Base64 string.
    :param video_file_path: Path to the video file.
    :return: Base64 encoded string.
    """
    with open(video_file_path, 'rb') as video_file:
        # Read the video file as binary
        video_bytes = video_file.read()

        # Encode binary data to Base64
        base64_encoded = base64.b64encode(video_bytes).decode('utf-8')

    return base64_encoded

print("*********************** step 2 ***************************")

with torch.inference_mode():
    model_id = "/content/model"
    transformer = CogVideoXTransformer3DModel.from_pretrained(model_id, subfolder="transformer", torch_dtype=torch.float16)
    text_encoder = T5EncoderModel.from_pretrained(model_id, subfolder="text_encoder", torch_dtype=torch.float16)
    vae = AutoencoderKLCogVideoX.from_pretrained(model_id, subfolder="vae", torch_dtype=torch.float16)
    tokenizer = T5Tokenizer.from_pretrained(model_id, subfolder="tokenizer")
    pipe = CogVideoXImageToVideoPipeline.from_pretrained(model_id, tokenizer=tokenizer, text_encoder=text_encoder, transformer=transformer, vae=vae, torch_dtype=torch.float16).to("cuda")
    # pipe.enable_model_cpu_offload()
print("*********************** step 3 ***************************")

def download_file(url, save_dir, file_name):
    os.makedirs(save_dir, exist_ok=True)
    original_file_name = url.split('/')[-1]
    _, original_file_extension = os.path.splitext(original_file_name)
    file_path = os.path.join(save_dir, file_name + original_file_extension)
    response = requests.get(url)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return file_path

@torch.inference_mode()
def generate(input):
    values = input["input"]
    print("*********************** step 4 ***************************")

    input_image = values['input_image']
    filename='input_image.jpg'
    decode_base64_and_save(input_image,filename)

    # input_image = download_file(url=input_image, save_dir='/content/input', file_name='input_image_tost')
    prompt = values['prompt']
    guidance_scale = values.get('guidance_scale',6)
    use_dynamic_cfg = values.get('use_dynamic_cfg',True)
    num_inference_steps = values.get('num_inference_steps',32)
    fps = values.get('fps',8)
    # guidance_scale = 6
    # use_dynamic_cfg = True
    # num_inference_steps = 50
    # fps = 8
    print("*********************** step 5 ***************************")

    image = load_image(filename)
    video = pipe(image=image, prompt=prompt, guidance_scale=guidance_scale, use_dynamic_cfg=use_dynamic_cfg, num_inference_steps=num_inference_steps).frames[0]
    export_to_video(video, "/content/cogvideox_5b_i2v_tost.mp4", fps=fps)
    print("*********************** step 6v***************************")

    result = "/content/cogvideox_5b_i2v_tost.mp4"
    enc_vid=encode_video_to_base64(result)
    return enc_vid

    # try:
    #     notify_uri = values['notify_uri']
    #     del values['notify_uri']
    #     notify_token = values['notify_token']
    #     del values['notify_token']
    #     discord_id = values['discord_id']
    #     del values['discord_id']
    #     if(discord_id == "discord_id"):
    #         discord_id = os.getenv('com_camenduru_discord_id')
    #     discord_channel = values['discord_channel']
    #     del values['discord_channel']
    #     if(discord_channel == "discord_channel"):
    #         discord_channel = os.getenv('com_camenduru_discord_channel')
    #     discord_token = values['discord_token']
    #     del values['discord_token']
    #     if(discord_token == "discord_token"):
    #         discord_token = os.getenv('com_camenduru_discord_token')
    #     job_id = values['job_id']
    #     del values['job_id']
    #     default_filename = os.path.basename(result)
    #     with open(result, "rb") as file:
    #         files = {default_filename: file.read()}
    #     payload = {"content": f"{json.dumps(values)} <@{discord_id}>"}
    #     response = requests.post(
    #         f"https://discord.com/api/v9/channels/{discord_channel}/messages",
    #         data=payload,
    #         headers={"Authorization": f"Bot {discord_token}"},
    #         files=files
    #     )
    #     response.raise_for_status()
    #     result_url = response.json()['attachments'][0]['url']
    #     notify_payload = {"jobId": job_id, "result": result_url, "status": "DONE"}
    #     web_notify_uri = os.getenv('com_camenduru_web_notify_uri')
    #     web_notify_token = os.getenv('com_camenduru_web_notify_token')
    #     if(notify_uri == "notify_uri"):
    #         requests.post(web_notify_uri, data=json.dumps(notify_payload), headers={'Content-Type': 'application/json', "Authorization": web_notify_token})
    #     else:
    #         requests.post(web_notify_uri, data=json.dumps(notify_payload), headers={'Content-Type': 'application/json', "Authorization": web_notify_token})
    #         requests.post(notify_uri, data=json.dumps(notify_payload), headers={'Content-Type': 'application/json', "Authorization": notify_token})
    #     return {"jobId": job_id, "result": result_url, "status": "DONE"}
    # except Exception as e:
    #     error_payload = {"jobId": job_id, "status": "FAILED"}
    #     try:
    #         if(notify_uri == "notify_uri"):
    #             requests.post(web_notify_uri, data=json.dumps(error_payload), headers={'Content-Type': 'application/json', "Authorization": web_notify_token})
    #         else:
    #             requests.post(web_notify_uri, data=json.dumps(error_payload), headers={'Content-Type': 'application/json', "Authorization": web_notify_token})
    #             requests.post(notify_uri, data=json.dumps(error_payload), headers={'Content-Type': 'application/json', "Authorization": notify_token})
    #     except:
    #         pass
    #     return {"jobId": job_id, "result": f"FAILED: {str(e)}", "status": "FAILED"}
    # finally:
    #     if os.path.exists(result):
    #         os.remove(result)
    #     if os.path.exists(input_image):
    #         os.remove(input_image)

runpod.serverless.start({"handler": generate})