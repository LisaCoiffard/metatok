import torch
from diffusers import StableDiffusionPipeline

device = "cuda:0"
pipe = StableDiffusionPipeline.from_pretrained(
    "friedrichor/stable-diffusion-2-1-realistic", torch_dtype=torch.float32
)
pipe.to(device)

prompt = "a woman in a red and gold costume with feathers on her head"
extra_prompt = ", facing the camera, photograph, highly detailed face, depth of field, moody light, style by Yasmin Albatoul, Harry Fayt, centered, extremely detailed, Nikon D850, award winning photography"
negative_prompt = "cartoon, anime, ugly, (aged, white beard, black skin, wrinkle:1.1), (bad proportions, unnatural feature, incongruous feature:1.4), (blurry, un-sharp, fuzzy, un-detailed skin:1.2), (facial contortion, poorly drawn face, deformed iris, deformed pupils:1.3), (mutated hands and fingers:1.5), disconnected hands, disconnected limbs"

generator = torch.Generator(device=device).manual_seed(42)
image = pipe(
    prompt + extra_prompt,
    negative_prompt=negative_prompt,
    height=768,
    width=768,
    num_inference_steps=20,
    guidance_scale=7.5,
    generator=generator,
).images[0]
image.save("image.png")
