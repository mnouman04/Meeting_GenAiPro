# 📝 Smart Meeting Minutes

> Transform your meeting recordings into actionable insights with AI

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev/)

## ✨ Features

- 🎤 **Audio Transcription** - Convert meeting recordings to text using OpenAI Whisper
- 🤖 **AI-Powered Analysis** - Generate comprehensive meeting minutes with Google Gemini
- ✅ **Action Items Extraction** - Automatically identify tasks, assignees, and deadlines
- 👥 **Participant Tracking** - Detect and list all meeting participants
- 📥 **Multiple Export Formats** - Download as TXT, JSON, or Markdown
- 🎯 **Decision Highlights** - Extract key decisions made during meetings
- 🎨 **Modern Dark Theme** - Premium UI with smooth animations

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for transcription)
- Google Gemini API key (for analysis)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Meeting_GenAiPro.git
   cd Meeting_GenAiPro
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (Optional)
   
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=sk-your-openai-key-here
   GEMINI_API_KEY=AIza-your-gemini-key-here
   ```

   Or enter them directly in the app's sidebar.

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Configure API Keys

- Enter your **OpenAI API key** in the sidebar (required for audio transcription)
- Enter your **Google Gemini API key** in the sidebar (required for minutes generation)
- Click "🧪 Test Gemini API" to verify your key works

### Step 2: Upload or Paste Content

**Option A: Upload Audio**
- Go to the "🎤 Upload Audio" tab
- Drag and drop your audio file (MP3, WAV, M4A, OGG, FLAC, WebM)
- Click "🚀 Transcribe Audio with AI"

**Option B: Paste Transcript**
- Go to the "✍️ Paste Transcript" tab
- Paste your meeting transcript
- Click "💾 Save Transcript"
- Or click "🧪 Load Demo" to try with sample data

### Step 3: Generate Minutes

- Go to the "📊 Results" tab
- Click "🚀 Generate Meeting Minutes with AI"
- Wait for AI to analyze and generate structured minutes

### Step 4: Download Results

Choose your preferred format:
- **📄 TXT** - Plain text format
- **📊 JSON** - Structured data format
- **📝 MD** - Markdown format

## 💰 Pricing

### OpenAI Whisper
- **$0.006 per minute** of audio
- Example: 10-minute meeting = **$0.06**

### Google Gemini
- ✅ **15 requests/min** (FREE)
- ✅ **1,500 requests/day** (FREE)
- ✅ **1 million tokens/day** (FREE)

**Total Cost:** ~$0.06 per 10-minute meeting (Gemini is FREE!)

## 🔑 Getting API Keys

### OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in
3. Create a new API key
4. Copy and paste into the app

### Google Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste into the app

## 🛠️ Technical Stack

- **Frontend:** Streamlit
- **Transcription:** OpenAI Whisper API
- **AI Analysis:** Google Gemini API
- **Language:** Python 3.8+
- **Styling:** Custom CSS with animations

## 📋 Output Format

The generated meeting minutes include:

- **Meeting Title** - Auto-generated descriptive title
- **Date** - Meeting date
- **Participants** - List of attendees
- **Executive Summary** - 2-3 sentence overview
- **Key Discussion Points** - Main topics discussed
- **Decisions Made** - Important decisions
- **Action Items** - Tasks with assignees and deadlines
- **Next Meeting** - Follow-up meeting info

## 🐛 Troubleshooting

### API Key Issues
- Verify your API keys are correct
- Check if Gemini API is enabled at [Google Cloud Console](https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com)
- Try creating a new API key

### Transcription Fails
- Ensure audio file is under 25 MB
- Check audio quality (clear speech, minimal background noise)
- Verify OpenAI API key has sufficient credits

### Generation Fails
- Check your Gemini API quota
- Ensure transcript is not empty
- Try with a shorter transcript first

## 📝 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

Built with ❤️ using Streamlit, OpenAI Whisper & Google Gemini