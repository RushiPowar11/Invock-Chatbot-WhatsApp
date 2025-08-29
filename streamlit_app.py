import streamlit as st
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Lead

st.set_page_config(page_title="Invock Leads Dashboard", layout="wide")
st.title("Invock Leads Dashboard")

# Database connection
@st.cache_data(ttl=60)  # Refresh every minute
def get_leads():
    session: Session = SessionLocal()
    try:
        leads = session.query(Lead).order_by(Lead.created_at.desc()).all()
        return leads
    finally:
        session.close()

# Get leads
leads = get_leads()

# Stats
if leads:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(leads))
    with col2:
        scheduled = len([l for l in leads if l.stage == "scheduled"])
        st.metric("Scheduled Demos", scheduled)
    with col3:
        completed = len([l for l in leads if l.full_name and l.email and l.business_name])
        st.metric("Complete Profiles", completed)
    with col4:
        pending = len([l for l in leads if l.stage not in ["scheduled", "start"]])
        st.metric("In Progress", pending)

# Leads table
if not leads:
    st.info("No leads yet. Start the WhatsApp bot to collect leads!")
else:
    # Convert to dataframe
    data = []
    for l in leads:
        data.append({
            "Phone": l.phone,
            "Name": l.full_name or "Not provided",
            "Email": l.email or "Not provided", 
            "Business": l.business_name or "Not provided",
            "Stage": l.stage,
            "Created": l.created_at.strftime("%Y-%m-%d %H:%M") if l.created_at else "N/A",
            "Updated": l.updated_at.strftime("%Y-%m-%d %H:%M") if l.updated_at else "N/A"
        })
    
    st.subheader("All Leads")
    st.dataframe(data, use_container_width=True)
    
    # Filter by stage
    st.subheader("Filter by Stage")
    stages = list(set([l.stage for l in leads]))
    selected_stage = st.selectbox("Select stage:", ["All"] + stages)
    
    if selected_stage != "All":
        filtered_leads = [l for l in leads if l.stage == selected_stage]
        if filtered_leads:
            filtered_data = []
            for l in filtered_leads:
                filtered_data.append({
                    "Phone": l.phone,
                    "Name": l.full_name or "Not provided",
                    "Email": l.email or "Not provided",
                    "Business": l.business_name or "Not provided",
                    "Created": l.created_at.strftime("%Y-%m-%d %H:%M") if l.created_at else "N/A"
                })
            st.dataframe(filtered_data, use_container_width=True)
        else:
            st.info(f"No leads in stage: {selected_stage}")

# Refresh button
if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()
