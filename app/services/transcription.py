from typing import Optional
import io
import json
import os
from google.cloud import speech_v1 as speech
from google.oauth2.service_account import Credentials
from ..config import settings


def _build_speech_client() -> speech.SpeechClient:
	# Prefer GOOGLE_APPLICATION_CREDENTIALS path for security
	gac_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
	if gac_path and os.path.exists(gac_path):
		return speech.SpeechClient()
	# Fallback to inline JSON in env (less secure; acceptable for prototypes)
	creds_dict = json.loads(settings.google_credentials_json or "{}")
	credentials = Credentials.from_service_account_info(creds_dict) if creds_dict else None
	return speech.SpeechClient(credentials=credentials) if credentials else speech.SpeechClient()


def transcribe_audio_bytes(audio_bytes: bytes, mime_type: str = "audio/ogg") -> Optional[str]:
	try:
		client = _build_speech_client()
		audio = {"content": audio_bytes}
		config = {
			"encoding": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
			"language_code": "en-US",
		}
		response = client.recognize(config=config, audio=audio)
		for result in response.results:
			if result.alternatives:
				return result.alternatives[0].transcript
		return None
	except Exception:
		return None
