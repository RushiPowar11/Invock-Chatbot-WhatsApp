import requests
from typing import Dict, Any, Optional
from ..config import settings

BASE_URL = "https://graph.facebook.com/v20.0"


def send_text_message(to_phone: str, text: str) -> Dict[str, Any]:
	url = f"{BASE_URL}/{settings.whatsapp_phone_number_id}/messages"
	headers = {
		"Authorization": f"Bearer {settings.whatsapp_access_token}",
		"Content-Type": "application/json",
	}
	payload = {
		"messaging_product": "whatsapp",
		"to": to_phone,
		"type": "text",
		"text": {"body": text},
	}
	resp = requests.post(url, headers=headers, json=payload, timeout=20)
	try:
		return resp.json()
	except Exception:
		return {"status_code": resp.status_code, "text": resp.text}


def get_media_url(media_id: str) -> Optional[str]:
	try:
		url = f"{BASE_URL}/{media_id}"
		headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
		resp = requests.get(url, headers=headers, timeout=20)
		data = resp.json()
		return data.get("url")
	except Exception:
		return None


def download_media(media_url: str) -> Optional[bytes]:
	try:
		headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
		resp = requests.get(media_url, headers=headers, timeout=30)
		if resp.status_code == 200:
			return resp.content
		return None
	except Exception:
		return None
