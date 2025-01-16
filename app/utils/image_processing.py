import requests
from pathlib import Path
from uuid import uuid4
from PIL import Image
from io import BytesIO
import logging

TEMP_DIR = "temp_images"
Path(TEMP_DIR).mkdir(exist_ok=True)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def process_images(image_urls, base_url):
    image_data = []

    for img_url in image_urls:
        if not img_url.startswith("http"):
            img_url = requests.compat.urljoin(base_url, img_url)
        try:
            image_response = requests.get(img_url, stream=True, timeout=5)
            if image_response.status_code == 200:
                img = Image.open(BytesIO(image_response.content))
                size = len(image_response.content)
                resolution = img.width * img.height
                image_data.append((resolution, size, image_response.content))
                logger.info(f"Processed image from: {img_url} with resolution {resolution} and size {size}")
            else:
                logger.warning(f"Failed to download image from: {img_url}")
        except Exception as img_error:
            logger.error(f"Error downloading image from {img_url}: {str(img_error)}")

    image_data = sorted(image_data, key=lambda x: (-x[0], -x[1]))[:5]
    image_paths = []

    for _, _, img_content in image_data:
        image_path = Path(TEMP_DIR) / f"{uuid4().hex}.jpg"
        with open(image_path, "wb") as f:
            f.write(img_content)
        image_paths.append(str(image_path))

    return image_paths