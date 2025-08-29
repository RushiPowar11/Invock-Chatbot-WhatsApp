# Invock WhatsApp Chatbot Prototype

A FastAPI-powered WhatsApp chatbot that handles inventory queries, collects lead information, and schedules demo meetings via Google Calendar. Features audio transcription using Google Speech-to-Text and AI responses via Gemini.

## 🏗️ Architecture

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI + SQLAlchemy |
| **Database** | PostgreSQL |
| **WhatsApp** | Meta WhatsApp Cloud API |
| **Calendar** | Google Calendar API |
| **AI/Transcription** | Gemini + Google Speech-to-Text |
| **Dashboard** | Streamlit |

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.8+
- PostgreSQL database
- Meta Developer Account (for WhatsApp)
- Google Cloud Project (for Calendar + Speech-to-Text)
- Gemini API key

### 2. Setup Environment
```bash
# Clone and navigate
git clone <your-repo>
cd invock-whatsapp-bot

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create `.env` file in project root:
```env
# Database
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/invock

# WhatsApp Cloud API
WHATSAPP_VERIFY_TOKEN=your_verify_token
WHATSAPP_ACCESS_TOKEN=your_whatsapp_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id

# Google Services
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
GOOGLE_CALENDAR_ID=primary
GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\credentials.json

# AI
GEMINI_API_KEY=your_gemini_key

```

### 4. Database Setup
```bash
# Create PostgreSQL database
createdb invock

# Tables are auto-created on startup
```

### 5. Run the Application
```bash
# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# In another terminal, start Streamlit dashboard
streamlit run streamlit_app.py
```

```

### 7. Configure WhatsApp Webhook
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Navigate to your WhatsApp app
3. Set webhook URL: `https://your-ngrok-url/webhook/whatsapp`
4. Verify token: Use the same `WHATSAPP_VERIFY_TOKEN` from your `.env`
5. Subscribe to `messages` events

## 🔧 Configuration Details

### WhatsApp Cloud API Setup
1. **Create App**: Meta for Developers → Create App → Business
2. **Add WhatsApp**: Products → WhatsApp → Getting Started
3. **Get Credentials**:
   - Phone Number ID
   - Access Token (System User, permanent)
   - Business Account ID
4. **Test Number**: Use the provided test phone number

### Google Cloud Setup
1. **Enable APIs**:
   - Google Calendar API
   - Cloud Speech-to-Text API
2. **Create Service Account**:
   - IAM & Admin → Service Accounts
   - Download JSON credentials
3. **Calendar Permissions**:
   - Share your calendar with service account email
   - Grant "Make changes to events" permission

### Database Configuration
- **Local**: Install PostgreSQL, create database
- **Cloud**: Use services like Supabase, Railway, or AWS RDS
- **Connection String**: `postgresql+psycopg2://user:pass@host:port/dbname`

## 📱 Usage Flows

### 1. Inventory Query Flow
```
User: "Do you help with inventory management?"
Bot: [Inventory capabilities + demo offer]
Bot: "Can I take your details for a demo?"
```

### 2. Lead Collection Flow
```
Bot: "May I have your full name?"
User: "John Doe"
Bot: "What's your email address?"
User: "john@example.com"
Bot: "What's your business name?"
User: "Acme Corp"
Bot: "What date/time works for a demo?"
```

### 3. Direct Demo Request
```
User: "Schedule a demo for tomorrow 2 PM"
Bot: [Collects missing details]
Bot: [Creates calendar event]
Bot: "Booked! Calendar invite: [link]"
```

### 4. Audio Message Flow
```
User: [Sends voice note]
Bot: [Transcribes audio via Google STT]
Bot: [Processes transcript as text]
Bot: [Continues conversation flow]
```

## 🗄️ Database Schema

### Lead Model
```python
class Lead(Base):
    id: Integer (Primary Key)
    phone: String (Unique, WhatsApp number)
    full_name: String
    email: String
    business_name: String
    stage: String (start|ask_name|ask_email|ask_business|ready_to_schedule|scheduled)
    created_at: DateTime
    updated_at: DateTime
```

## 📊 Dashboard Features

- **Real-time Stats**: Total leads, scheduled demos, complete profiles
- **Lead Table**: All leads with filtering by stage
- **Auto-refresh**: Data updates every minute
- **Stage Filtering**: View leads by conversation stage

## 🔒 Security Features

- Environment variables for all secrets
- `.gitignore` excludes `.env` and credential files
- Service account authentication for Google APIs
- WhatsApp webhook verification

## 🚀 Deployment

### Local Development
```bash
uvicorn app.main:app --reload --port 8000
```

### Cloud Deployment
1. **Render**: Connect GitHub repo, set environment variables
2. **Railway**: Deploy from GitHub, configure env vars
3. **Fly.io**: Use Dockerfile, set secrets
4. **Vercel**: Deploy as serverless functions

### Environment Variables in Production
- Use your platform's secret manager
- Never commit `.env` files
- Set `PUBLIC_BASE_URL` to your domain

## 🧪 Testing

### Test Webhook Verification
```bash
curl "http://localhost:8000/webhook/whatsapp?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=test"
```

### Test Message Handling
1. Send message from WhatsApp test number
2. Check logs for webhook processing
3. Verify database entry creation
4. Check calendar event creation

## 📝 API Endpoints

- `GET /webhook/whatsapp` - WhatsApp webhook verification
- `POST /webhook/whatsapp` - WhatsApp message handling
- `GET /docs` - FastAPI auto-generated documentation

## 🔍 Troubleshooting

### Common Issues
1. **Webhook Verification Fails**
   - Check `WHATSAPP_VERIFY_TOKEN` matches
   - Ensure webhook URL is accessible

2. **Database Connection Error**
   - Verify `DATABASE_URL` format
   - Check PostgreSQL is running
   - Ensure database exists

3. **Calendar Creation Fails**
   - Verify service account permissions
   - Check `GOOGLE_CALENDAR_ID`
   - Ensure credentials JSON is valid

4. **Audio Transcription Issues**
   - Check Google Cloud Speech-to-Text API is enabled
   - Verify service account has Speech-to-Text permissions

### Logs
- FastAPI logs show webhook processing
- Check database queries in SQLAlchemy logs
- Google API errors appear in service responses

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is for demonstration purposes. Ensure compliance with WhatsApp Business API terms and Google Cloud usage policies.

## 🆘 Support

For issues:
1. Check the troubleshooting section
2. Verify environment variables
3. Test individual components
4. Check API documentation links
