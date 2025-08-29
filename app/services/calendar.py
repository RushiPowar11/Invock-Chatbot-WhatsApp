from typing import Optional, Tuple
from dateutil import parser as dateparser
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from datetime import timedelta
import json
from ..config import settings


SCOPES = ["https://www.googleapis.com/auth/calendar"]


def parse_datetime(user_input: str) -> Optional[Tuple[str, str]]:
	try:
		dt = dateparser.parse(user_input, fuzzy=True)
		if not dt:
			return None
		start = dt.isoformat()
		end_dt = dt + timedelta(minutes=30)
		end = end_dt.isoformat()
		return start, end
	except Exception:
		return None


def create_calendar_event(summary: str, description: str, start_iso: str, end_iso: str) -> Optional[str]:
	try:
		creds_dict = json.loads(settings.google_credentials_json or "{}")
		creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
		service = build("calendar", "v3", credentials=creds)

		event_body = {
			"summary": summary,
			"description": description,
			"start": {"dateTime": start_iso},
			"end": {"dateTime": end_iso or start_iso},
		}
		event = service.events().insert(calendarId=settings.calendar_id, body=event_body).execute()
		return event.get("htmlLink")
	except Exception:
		return None
