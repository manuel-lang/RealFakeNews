import time
from logging.config import dictConfig
import logging
from config import LogConfig

from models import APIInput
from text_processing import summarize_text
from typing import Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from text_to_speech import TextToAudio
from speech_to_video import SpeechToVideo
from fastapi import Response

from shutil import copyfile

dictConfig(LogConfig().dict())
logger = logging.getLogger("deep-fake-news")

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    text_summary = request_data.text
    logger.info(f'Summarize? {request_data.summarize}')
    if request_data is not None and request_data.summarize:
        text_summary = summarize_text(
            text=request_data.text, min_words=request_data.min_text_length, max_words=request_data.max_text_length)

    logger.info("Creating audio...")
    text_to_audio = TextToAudio(
        output_path=str(int(time.time())),
        output_name='audio.wav',
        rate=22050
    )
    logger.info(f'Converting "{text_summary}" into audio.')
    output_audio_path = text_to_audio.parse_text(text_to_convert=text_summary)
    logger.info(f'The generated audio file is in {output_audio_path}.')

    logger.info("Creating video...")
    speech_to_video = SpeechToVideo(
        output_path='/app/output_video/',
        output_name='output_video.mp4',
    )
    output_path_video = speech_to_video.generate_video(model_path="/app/model_checkpoints/wav2lip.pth", video_path="/app/input_video/output_video.mp4", audio_path=output_audio_path)
    logger.info(f'The generated audio file is in {output_path_video} .')

    new_output_path_video = f'../ui/public/{output_path_video.split("/")[-1]}'
    copyfile(output_path_video, new_output_path_video)

    # return FileResponse(output_path_video)
    return {'url': new_output_path_video.split("/")[-1]}
