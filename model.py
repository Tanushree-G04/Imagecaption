# virtualenv venv
# source venv/Scripts/activate

# python -m pip install git+https://github.com/huggingface/transformers.git
# python -m pip install pillow
# python -m pip install torch torchvision torchaudio
# python -m pip install streamlit
# python -m pip install filetype

# python imagecap.py
# isort .
# black .

from PIL import Image
from transformers import BlipForConditionalGeneration, BlipProcessor

from config import IMAGE_PATH

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def image_caption_generator(img_url):
    raw_image = Image.open(img_url).convert("RGB")

    # conditional image captioning
    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    text = processor.decode(out[0], skip_special_tokens=True)

    return text


if __name__ == "__main__":
    import pathlib

    FILE_PATH = pathlib.Path(__file__)
    BASE_FILE = FILE_PATH.parent.absolute()

    text = image_caption_generator(IMAGE_PATH)
    print(text)
