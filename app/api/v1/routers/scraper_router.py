from fastapi import APIRouter, Query
from app.services.scraper_service import scrape_and_send_email
import logging

router = APIRouter()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@router.get("/scrape")
async def scrape_url(url: str = Query(..., title="URL to scrape", example="https://example.com")):
    try:
        logger.info(f"Received request to scrape URL: {url}")
        result = await scrape_and_send_email(url)
        logger.info(f"Successfully sent email for URL: {url}")
        return {"detail": "Email sent successfully", "result": result}
    except Exception as e:
        logger.error(f"Error processing URL: {url}, Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))