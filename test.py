import streamlit as st
import google.generativeai as genai
from openai import OpenAI
from datetime import datetime
import json
import tempfile
import os
from dotenv import load_dotenv

load_dotenv()

# Page config MUST be first Streamlit command
st.set_page_config(
    page_title="Smart Meeting Minutes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Inter', sans-serif !important;
    }
    
    html, body {
        background: #0a0a0a;
        color: #f5f1ff;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #16213e 100%);
    }
    
    .main {
        padding: 0 !important;
    }
    
    .main > div {
        padding: 2.5rem !important;
    }
    
    section[data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a0a2e 50%, #16213e 100%);
    }
    
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    /* Premium animation keyframes */
    @keyframes slideInDown {
        from {
            opacity: 0;
            transform: translateY(-40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(25px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulseGlow {
        0%, 100% {
            text-shadow: 0 0 20px rgba(233, 179, 251, 0.3), 0 0 40px rgba(111, 0, 255, 0.2);
        }
        50% {
            text-shadow: 0 0 30px rgba(233, 179, 251, 0.6), 0 0 60px rgba(111, 0, 255, 0.4);
        }
    }
    
    @keyframes smoothBorder {
        0% {
            border-color: rgba(111, 0, 255, 0.3);
        }
        50% {
            border-color: rgba(233, 179, 251, 0.6);
        }
        100% {
            border-color: rgba(111, 0, 255, 0.3);
        }
    }
    
    /* Main heading - MUCH LARGER and prominent */
    h1 {
        background: linear-gradient(135deg, #8B5CF6, #EC4899, #6F00FF, #8B5CF6);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 4.2rem !important;
        font-weight: 900 !important;
        text-align: center;
        margin-bottom: 0.3rem !important;
        letter-spacing: -1px !important;
        animation: slideInDown 0.9s cubic-bezier(0.34, 1.56, 0.64, 1), gradientShift 4s ease-in-out infinite !important;
        line-height: 1.1 !important;
    }
    
    /* Subtitle with enhanced styling */
    .subtitle {
        text-align: center;
        color: #e9b3fb !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 1.35rem !important;
        font-weight: 500 !important;
        margin-bottom: 2.5rem !important;
        animation: fadeInUp 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.2s both !important;
        letter-spacing: 0.3px !important;
    }
    
    h2 {
        color: #f5f1ff !important;
        font-family: 'Poppins', sans-serif !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        animation: fadeInUp 0.7s ease-out !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
    }
    
    h3 {
        color: #d4a5ff !important;
        font-family: 'Poppins', sans-serif !important;
        font-weight: 600 !important;
        animation: fadeInUp 0.6s ease-out !important;
        transition: color 0.4s ease !important;
    }
    
    h4 {
        color: #e9b3fb !important;
        font-weight: 600 !important;
    }
    
    /* Generated content text - OFF-WHITE for visibility */
    .generated-content {
        color: #f5f1ff !important;
        background: rgba(20, 15, 40, 0.7) !important;
        border: 1px solid rgba(111, 0, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        line-height: 1.7 !important;
        font-size: 1rem !important;
        animation: fadeInUp 0.7s ease-out !important;
        transition: all 0.4s ease !important;
    }
    
    .generated-content:hover {
        border-color: rgba(233, 179, 251, 0.4) !important;
        background: rgba(20, 15, 40, 0.9) !important;
    }
    
    p, label, span {
        color: #e0d5ff !important;
    }
    
    /* Header section with image */
    .header-section {
        position: relative;
        height: 320px;
        border-radius: 18px;
        overflow: hidden;
        margin-bottom: 2.5rem;
        box-shadow: 0 15px 50px rgba(111, 0, 255, 0.25);
        animation: fadeInUp 0.7s ease-out !important;
        border: 2px solid rgba(233, 179, 251, 0.1);
        transition: all 0.5s cubic-bezier(0.25, 0.46, 0.45, 0.94);
    }
    
    .header-section:hover {
        box-shadow: 0 20px 70px rgba(111, 0, 255, 0.35);
        border-color: rgba(233, 179, 251, 0.2);
        transform: translateY(-2px);
    }
    
    .header-image {
        width: 100%;
        height: 100%;
        object-fit: cover;
        filter: brightness(0.65) contrast(1.15) saturate(1.1);
        transition: filter 0.6s ease !important;
    }
    
    .header-section:hover .header-image {
        filter: brightness(0.75) contrast(1.2) saturate(1.2);
    }
    
    .header-overlay {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(111, 0, 255, 0.35), rgba(59, 2, 112, 0.55));
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .header-title {
        font-family: 'Poppins', sans-serif !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        text-align: center;
        text-shadow: 0 6px 20px rgba(0, 0, 0, 0.6);
        animation: slideInDown 0.9s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        letter-spacing: -0.5px !important;
    }
    
    .header-subtitle {
        font-size: 1.1rem !important;
        color: #e9b3fb !important;
        text-align: center;
        text-shadow: 0 3px 12px rgba(0, 0, 0, 0.6);
        margin-top: 0.7rem;
        animation: fadeInUp 0.9s cubic-bezier(0.25, 0.46, 0.45, 0.94) 0.2s both !important;
        font-weight: 500 !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6, #6F00FF) !important;
        color: white !important;
        border: 2px solid #6F00FF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 0.85rem 1.8rem !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        box-shadow: 0 6px 30px rgba(111, 0, 255, 0.4) !important;
        font-size: 1rem !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.02) !important;
        box-shadow: 0 12px 50px rgba(111, 0, 255, 0.6) !important;
        background: linear-gradient(135deg, #A78BFA, #7C3AED) !important;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    .stTextInput > div > div > input {
        background: rgba(15, 15, 35, 0.7) !important;
        border: 2px solid rgba(111, 0, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #f5f1ff !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(233, 179, 251, 0.5) !important;
        box-shadow: 0 0 15px rgba(111, 0, 255, 0.2) !important;
        background: rgba(15, 15, 35, 0.9) !important;
    }
    
    .stTextArea > div > div > textarea {
        background: rgba(15, 15, 35, 0.7) !important;
        border: 2px solid rgba(111, 0, 255, 0.2) !important;
        border-radius: 10px !important;
        color: #f5f1ff !important;
        font-family: 'Monaco', monospace !important;
        transition: all 0.3s ease !important;
        font-size: 1rem !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: rgba(233, 179, 251, 0.5) !important;
        box-shadow: 0 0 15px rgba(111, 0, 255, 0.2) !important;
        background: rgba(15, 15, 35, 0.9) !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        background-color: rgba(26, 10, 46, 0.5) !important;
        border-radius: 12px !important;
        border-bottom: 2px solid rgba(111, 0, 255, 0.1) !important;
        gap: 0.5rem !important;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px !important;
        color: #9d88b8 !important;
        transition: all 0.4s ease !important;
        font-weight: 600 !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(111, 0, 255, 0.3), rgba(59, 2, 112, 0.2)) !important;
        color: #e9b3fb !important;
        border-bottom: 3px solid #6F00FF !important;
    }
    
    .success-card {
        background: linear-gradient(135deg, rgba(34, 197, 94, 0.15), rgba(34, 197, 94, 0.08)) !important;
        border-left: 4px solid #22c55e !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
        color: #86efac !important;
        animation: fadeInUp 0.5s ease-out !important;
        font-weight: 500 !important;
    }
    
    .info-card {
        background: linear-gradient(135deg, rgba(111, 0, 255, 0.15), rgba(59, 2, 112, 0.1)) !important;
        border-left: 4px solid #8B5CF6 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
        color: #e9b3fb !important;
        animation: fadeInUp 0.5s ease-out !important;
        font-weight: 500 !important;
    }
    
    .warning-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(239, 68, 68, 0.08)) !important;
        border-left: 4px solid #ef4444 !important;
        border-radius: 10px !important;
        padding: 1.2rem !important;
        color: #fca5a5 !important;
        animation: fadeInUp 0.5s ease-out !important;
        font-weight: 500 !important;
    }
    
    a {
        color: #8B5CF6 !important;
        text-decoration: none !important;
        transition: color 0.3s ease !important;
    }
    
    a:hover {
        color: #e9b3fb !important;
    }
    </style>
""", unsafe_allow_html=True)

# Get API keys from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY", "")
gemini_api_key = os.getenv("GEMINI_API_KEY", "")

# Verify API keys are configured
if not openai_api_key or not gemini_api_key:
    st.error("⚠️ Missing API Keys! Please configure OPENAI_API_KEY and GEMINI_API_KEY environment variables.")
    st.stop()

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = ''
if 'minutes' not in st.session_state:
    st.session_state.minutes = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# Main Header
st.markdown("<h1>📝 Smart Meeting Minutes</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>✨ Transform your meeting recordings into actionable insights with AI ✨</p>", unsafe_allow_html=True)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["🎤 Upload Audio", "✍️ Paste Transcript", "📊 Results"])

with tab1:
    # Header with background image
    st.markdown("""
        <div class='header-section'>
            <img src='https://images.unsplash.com/photo-1552664730-d307ca884978?w=1200&h=400&fit=crop' class='header-image' alt='Audio Recording'>
            <div class='header-overlay'>
                <div class='header-title'>🎤 Upload Meeting Recording</div>
                <div class='header-subtitle'>Convert your audio files into transcriptions instantly</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        audio_file = st.file_uploader(
            "Drop your audio file here",
            type=['mp3', 'wav', 'm4a', 'ogg', 'flac', 'webm'],
            help="Supported: MP3, WAV, M4A, OGG, FLAC, WebM"
        )
        
        if audio_file:
            file_size_mb = audio_file.size / (1024 * 1024)
            st.markdown(f"""
                <div class='success-card'>
                    <strong>✅ File Uploaded Successfully</strong><br/>
                    📁 {audio_file.name} | 💾 {file_size_mb:.2f} MB
                </div>
            """, unsafe_allow_html=True)
            
            st.audio(audio_file)
            
            if st.button("🚀 Transcribe Audio with AI", key="transcribe_btn", use_container_width=True):
                with st.spinner("🎯 Transcribing audio... Please wait..."):
                    try:
                        client = OpenAI(api_key=openai_api_key)
                        
                        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(audio_file.name)[1]) as tmp_file:
                            tmp_file.write(audio_file.getvalue())
                            tmp_file_path = tmp_file.name
                        
                        with open(tmp_file_path, "rb") as audio_data:
                            transcript_response = client.audio.transcriptions.create(
                                model="whisper-1",
                                file=audio_data,
                                response_format="text"
                            )
                        
                        os.unlink(tmp_file_path)
                        st.session_state.transcript = transcript_response
                        st.markdown('<div class="success-card"><strong>✅ Transcription completed!</strong></div>', unsafe_allow_html=True)
                        st.balloons()
                        st.rerun()
                        
                    except Exception as e:
                        st.markdown(f'<div class="warning-card"><strong>❌ Transcription failed: {str(e)[:100]}</strong></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='info-card'>
                <strong>💡 Tips</strong><br/><br/>
                ✓ Clear audio quality<br/>
                ✓ Low background noise<br/>
                ✓ Max: 25 MB<br/>
                ✓ MP3, WAV, M4A
            </div>
        """, unsafe_allow_html=True)

with tab2:
    # Header with background image
    st.markdown("""
        <div class='header-section'>
            <img src='https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=1200&h=400&fit=crop' class='header-image' alt='Transcript'>
            <div class='header-overlay'>
                <div class='header-title'>✍️ Paste Meeting Transcript</div>
                <div class='header-subtitle'>Enter your meeting transcript and generate AI-powered minutes</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        transcript_input = st.text_area(
            "Paste your meeting transcript here:",
            value=st.session_state.transcript,
            height=400,
            placeholder="Enter or paste your meeting transcript here..."
        )
    
    with col2:
        if st.button("💾 Save Transcript", key="save_transcript", use_container_width=True):
            if transcript_input.strip():
                st.session_state.transcript = transcript_input
                st.markdown('<div class="success-card"><strong>✅ Saved!</strong></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="warning-card"><strong>⚠️ Enter text first</strong></div>', unsafe_allow_html=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        if st.button("🧪 Load Demo", key="demo_btn", use_container_width=True):
            st.session_state.transcript = """Welcome everyone to today's product planning meeting.

John: Thanks for joining. Today we discuss Q1 roadmap, customer feature requests, and sprint planning.

Sarah: The mobile app prototype got great feedback. We should prioritize push notifications - customers have requested it.

Mike: Agreed on Sarah's point. Analytics dashboard is gaining traction too. But we need infrastructure upgrades for increased load.

John: Good point Mike. Add infrastructure to action items. Sarah, lead push notifications?

Sarah: Absolutely. 3 weeks needed. I'll coordinate with design this week.

Mike: I'll assess infrastructure and present options by Monday.

Lisa: We have 5 requests for dark mode. Should we include this in Q1?

John: Let's evaluate. Lisa, compile feedback and business case by Friday?

Lisa: Will do.

John: Summary: Sarah on push notifications, Mike on infrastructure, Lisa on dark mode case. Meet Tuesday. Thanks!"""
            st.markdown('<div class="success-card"><strong>✅ Demo loaded!</strong></div>', unsafe_allow_html=True)
            st.rerun()

# TAB 3: Results
with tab3:
    if st.session_state.transcript:
        
        with st.expander("📄 View Original Transcript", expanded=False):
            st.text_area("Transcript Content", st.session_state.transcript, height=300, disabled=True)
        
        st.markdown("<br/>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🚀 Generate Meeting Minutes with AI", key="generate_btn", use_container_width=True):
                with st.spinner("🤖 Generating minutes with AI..."):
                    try:
                        genai.configure(api_key=gemini_api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        
                        prompt = f"""Analyze this meeting transcript and generate comprehensive meeting minutes:

MEETING SUMMARY
===============
[2-3 sentence overview]

KEY DISCUSSION POINTS
====================
- Point 1
- Point 2
- Point 3

ACTION ITEMS
============
[ ] Owner: Task - Due date
[ ] Owner: Task - Due date

DECISIONS MADE
==============
- Decision 1
- Decision 2

PARTICIPANTS
============
[List of people]

NEXT STEPS
==========
[Key follow-ups]

Transcript:
{st.session_state.transcript}"""
                        
                        response = model.generate_content(prompt)
                        st.session_state.minutes = response.text
                        
                        st.markdown('<div class="success-card"><strong>✅ Minutes generated successfully!</strong></div>', unsafe_allow_html=True)
                        st.rerun()
                        
                    except Exception as e:
                        st.markdown(f'<div class="warning-card"><strong>❌ Generation failed: {str(e)[:80]}</strong></div>', unsafe_allow_html=True)
        
        if st.session_state.minutes:
            st.markdown("---")
            st.markdown("<h2>📋 Generated Meeting Minutes</h2>", unsafe_allow_html=True)
            st.markdown(f'<div class="generated-content">{st.session_state.minutes}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                txt_data = st.session_state.minutes
                st.download_button(
                    label="📥 Download as TXT",
                    data=txt_data,
                    file_name=f"minutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            
            with col2:
                json_data = {
                    "timestamp": datetime.now().isoformat(),
                    "transcript": st.session_state.transcript,
                    "minutes": st.session_state.minutes
                }
                st.download_button(
                    label="📥 Download as JSON",
                    data=json.dumps(json_data, indent=2),
                    file_name=f"minutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json",
                    use_container_width=True
                )
    else:
        st.markdown("""
            <div class='info-card'>
                <strong>📝 No transcript yet</strong><br/><br/>
                1. Upload audio or paste transcript<br/>
                2. Click "Generate Minutes"<br/>
                3. Download results
            </div>
        """, unsafe_allow_html=True)
