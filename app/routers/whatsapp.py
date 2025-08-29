from fastapi import APIRouter, Request, Depends
from fastapi.responses import PlainTextResponse
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import Lead
from ..services.whatsapp import send_text_message, get_media_url, download_media
from ..services.inventory import answer_inventory_question
from ..services.lead_flow import handle_lead_message
from ..services.transcription import transcribe_audio_bytes

router = APIRouter()


@router.get("/whatsapp", response_class=PlainTextResponse)
def verify_whatsapp(request: Request):
	params = request.query_params
	mode = params.get("hub.mode")
	token = params.get("hub.verify_token")
	challenge = params.get("hub.challenge")
	if mode == "subscribe" and token == settings.whatsapp_verify_token:
		return PlainTextResponse(content=challenge or "", status_code=200)
	return PlainTextResponse(content="forbidden", status_code=403)


@router.post("/whatsapp")
async def receive_message(req: Request, db: Session = Depends(get_db)):
	body = await req.json()
	try:
		entry = (body.get("entry") or [])[0]
		changes = (entry.get("changes") or [])[0]
		value = changes.get("value", {})
		messages = value.get("messages") or []
		if not messages:
			return {"status": "ok"}
		msg = messages[0]
		from_phone = msg.get("from")
		text = ""

		lead = db.query(Lead).filter(Lead.phone == from_phone).first()
		if not lead:
			lead = Lead(phone=from_phone, stage="start")
			db.add(lead)
			db.commit()
			db.refresh(lead)

		if msg.get("type") == "text":
			text = msg.get("text", {}).get("body", "")
		elif msg.get("type") == "audio":
			audio_info = msg.get("audio", {})
			media_id = audio_info.get("id")
			if media_id:
				media_url = get_media_url(media_id)
				if media_url:
					media_bytes = download_media(media_url)
					if media_bytes:
						transcript = transcribe_audio_bytes(media_bytes, mime_type=audio_info.get("mime_type", "audio/ogg"))
						if transcript:
							text = transcript
		if not text:
			send_text_message(from_phone, "I received your message but couldn't read it. Please send text.")
			return {"status": "ok"}

		# Inventory responder can short-circuit with an answer and move to lead capture
		inv_answer = answer_inventory_question(text)
		if inv_answer:
			send_text_message(from_phone, inv_answer)
			lead.stage = "ask_name" if not lead.full_name else ("ask_email" if not lead.email else ("ask_business" if not lead.business_name else "ready_to_schedule"))
			db.commit()
			return {"status": "ok"}

		# Lead flow handler returns next prompt and possibly triggers scheduling
		reply = handle_lead_message(text, lead, db)
		if reply:
			send_text_message(from_phone, reply)
		return {"status": "ok"}
	except Exception:
		return {"status": "ignored"}
