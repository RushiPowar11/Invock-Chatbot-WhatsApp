import re
from typing import Optional
from sqlalchemy.orm import Session
from ..models import Lead
from .calendar import parse_datetime, create_calendar_event

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _normalize(text: str) -> str:
	return (text or "").strip()


def _is_schedule_intent(text: str) -> bool:
	lt = text.lower()
	return any(k in lt for k in ["demo", "schedule", "book", "meeting", "call", "calendar"]) 


def handle_lead_message(user_text: str, lead: Lead, db: Session) -> Optional[str]:
	text = _normalize(user_text)

	# Flexible entry: if user asks to schedule at any time
	if _is_schedule_intent(text):
		lead.stage = lead.stage or "start"
		if not lead.full_name:
			lead.stage = "ask_name"
			db.commit()
			return "Great! Can I have your full name?"
		if not lead.email:
			lead.stage = "ask_email"
			db.commit()
			return "Thanks. What's your email address?"
		if not lead.business_name:
			lead.stage = "ask_business"
			db.commit()
			return "Got it. What's your business name?"
		lead.stage = "ready_to_schedule"
		db.commit()
		return "What date and time works for you? (e.g., 25 Aug, 3 PM)"

	# Regular staged flow
	stage = lead.stage or "start"
	if stage == "start":
		lead.stage = "ask_name"
		db.commit()
		return "Hi! I can help set up a demo for Invock's inventory management. May I have your full name?"

	if stage == "ask_name":
		lead.full_name = text
		lead.stage = "ask_email"
		db.commit()
		return f"Thanks, {lead.full_name}. What's your email address?"

	if stage == "ask_email":
		if not EMAIL_RE.match(text):
			return "That email doesn't look right. Please re-enter your email."
		lead.email = text
		lead.stage = "ask_business"
		db.commit()
		return "Great. What's your business name?"

	if stage == "ask_business":
		lead.business_name = text
		lead.stage = "ready_to_schedule"
		db.commit()
		return "Thanks! What date and time suits you for a demo? (e.g., 25 Aug, 3 PM)"

	if stage == "ready_to_schedule":
		parsed = parse_datetime(text)
		if not parsed:
			return "I couldn't understand the time. Please try a format like '25 Aug, 3 PM'."
		start_iso, end_iso = parsed
		link = create_calendar_event(
			summary=f"Invock Demo with {lead.full_name}",
			description=f"Lead: {lead.full_name} | Email: {lead.email} | Business: {lead.business_name}",
			start_iso=start_iso,
			end_iso=end_iso,
		)
		if link:
			lead.stage = "scheduled"
			db.commit()
			return f"Booked! Calendar invite created. Details: {link}"
		return "I couldn't create the calendar event right now. I'll try again later or we can pick another time."

	return None
