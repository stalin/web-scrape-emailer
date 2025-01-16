import requests
from bs4 import BeautifulSoup
from app.utils.email import send_email
from app.utils.image_processing import process_images
from fastapi import HTTPException
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def scrape_and_send_email(url: str):
    try:
        logger.info(f"Starting to scrape URL: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logger.info(f"Successfully fetched URL: {url}")

        soup = BeautifulSoup(response.text, "html.parser")

        subject = soup.title.string if soup.title else "Web Scraped Content"
        body = soup.get_text("\n", strip=True)

        if not body.strip():
            logger.warning(f"No content found at URL: {url}")
            raise ValueError("The URL does not contain any visible content.")

        image_urls = [img["src"] for img in soup.find_all("img") if img.get("src")]

        image_paths = process_images(image_urls, base_url=url)

        send_email(
            subject=subject,
            body=body,
            attachments=image_paths
        )

        logger.info(f"Email sent successfully for URL: {url}")
        return {"subject": subject, "images_attached": len(image_paths)}
    except requests.exceptions.RequestException as req_error:
        logger.error(f"Network error while accessing URL: {url}, Error: {str(req_error)}")
        raise HTTPException(status_code=400, detail="Failed to fetch the URL. Please check the URL and try again.")
    except Exception as e:
        logger.error(f"Error processing URL: {url}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error scraping URL: {str(e)}")