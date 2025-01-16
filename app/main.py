from fastapi import FastAPI, Depends, HTTPException
from app.api.v1.routers.scraper_router import router as scraper_router

app = FastAPI(title="Web Scraper Emailer")

app.include_router(scraper_router, prefix="/api/v1/scraper")
