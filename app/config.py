import os
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

class Settings(BaseModel):
	database_url: str = os.getenv("DATABASE_URL","")
	whatsapp_verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
	whatsapp_access_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
	whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
	google_credentials_json: str = os.getenv("GOOGLE_CREDENTIALS_JSON", "")
	calendar_id: str = os.getenv("GOOGLE_CALENDAR_ID", "primary")
	gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")

settings = Settings()
