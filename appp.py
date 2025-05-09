import streamlit as st
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# --- Streamlit Page Setup ---
st.set_page_config(page_title="🎥 YouTube Video Summarizer")
st.title("🎥 YouTube Transcript to Detailed Notes Converter")

# --- Sidebar: API Key Input ---
st.sidebar.title("🔑 API Key Configuration")
api_key = st.sidebar.text_input("Enter your Google API Key", type="password")

# --- Check for API Key ---
if not api_key:
    st.warning("Please enter your Google API key in the sidebar to continue.")
    st.stop()
else:
    genai.configure(api_key=api_key)

# --- Prompt Template ---
prompt = """
You are an expert content summarizer specializing in analyzing and condensing long-form YouTube video transcripts. 
Your task is to create a concise yet comprehensive summary based only on the transcript provided. 

Instructions:
1. Summarize the key points of the video in bullet format (✓ or •).
2. Highlight the main ideas, arguments, or steps discussed in the video.
3. Avoid unnecessary filler content or repetition from the transcript.
4. Maintain the original intent and tone of the video (informative, tutorial, motivational, etc.).
5. Limit the summary to **250 words or fewer**.
6. Ensure that the summary is easy to read and useful as study notes or a reference.

Here is the transcript to summarize:
"""

# --- Extract Transcript Function ---
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[1].split("&")[0]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([entry["text"] for entry in transcript_text])
        return transcript, video_id
    except Exception as e:
        st.error(f"Error extracting transcript: {str(e)}")
        return None, None

# --- Generate Summary Function ---
def generate_gemini_content(transcript_text, prompt):
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    response = model.generate_content([prompt + transcript_text])
    return response.text

# --- Input Field for YouTube Link ---
youtube_link = st.text_input("🔗 Enter YouTube Video Link:")

if youtube_link:
    _, video_id_preview = extract_transcript_details(youtube_link)
    if video_id_preview:
        st.image(f"http://img.youtube.com/vi/{video_id_preview}/0.jpg", use_container_width=True)

# --- Button to Generate Summary ---
if st.button("📝 Get Detailed Notes"):
    transcript_text, _ = extract_transcript_details(youtube_link)

    if transcript_text:
        with st.spinner("Generating summary..."):
            summary = generate_gemini_content(transcript_text, prompt)
            st.markdown("## 📋 Detailed Summary")
            st.write(summary)
    else:
        st.warning("Could not retrieve transcript. Please check the video link.")
