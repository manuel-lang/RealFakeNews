from logging.config import dictConfig
import logging
from .config import LogConfig

from models import APIInput
from text_processing import summarize_text
from typing import Dict

from logger_conf import log_config

from fastapi import FastAPI

dictConfig(LogConfig().dict())
logger = logging.getLogger("deep-fake-news")

app = FastAPI(debug=True)


@app.post("/")
def create_video(request_data: APIInput) -> Dict:
    """
    Creates a news video based on provided text information

    Args:
        request_data (APIInput): required API information

    Returns:
        Dict: JSON response data
    """
    logger.info("Creating text summary...")
    text_summary = summarize_text(
        text=request_data.text, min_words=request_data.min_text_length, max_words=request_data.max_text_length)

    logger.info("Creating audio...")
    # Create audio

    logger.info("Creating video...")
    # Create video

    return {"Hello": "World"}
