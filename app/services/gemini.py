from typing import Optional
import google.generativeai as genai
from ..config import settings


def init_client():
	genai.configure(api_key=getattr(settings, "gemini_api_key", None) or "")


def generate_response(prompt: str, model: str = "gemini-2.0-flash") -> Optional[str]:
	try:
		init_client()
		mdl = genai.GenerativeModel(model)
		resp = mdl.generate_content(prompt)
		return resp.text if hasattr(resp, "text") else None
	except Exception:
		return None
