import streamlit as st
import tempfile
import os
from twelvelabs import TwelveLabs
from utils import (
    API_KEY, process_video, fetch_existing_videos,
    get_video_url, get_hls_player_html, generate_timestamps
)

# Set up the Streamlit page configuration
st.set_page_config(page_title="YouTube Chapter Timestamp Generator", layout="wide")

# Add custom CSS for page styling
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/free-vector/vibrant-summer-ombre-background-vector_53876-105765.jpg");
    background-size: cover;
}
[data-testid="stHeader"] {
    background-color: rgba(0,0,0,0);
}
[data-testid="stToolbar"] {
    right: 2rem;
    background-image: url("");
    background-size: cover;
}
</style>
""", unsafe_allow_html=True)

# Add page title and separator with markdown
st.markdown("<h2 style='text-align: center;'>YouTube Chapter Timestamp Generator ✍</h2>", unsafe_allow_html=True)
st.markdown("---")


# Utility function for uploading and processing of new videos
def upload_and_process_video():

    video_type = st.selectbox("Select video type:", ["Basic Video (less than 30 mins)", "Podcast (30 mins to 1 hour)"])
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file and st.button("Process Video"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        try:
            with st.spinner("Processing video..."):
                client = TwelveLabs(api_key=API_KEY)
                timestamps = process_video(client, video_path, video_type)
            st.success("Video processed successfully!")
            st.subheader("YouTube Chapter Timestamps")
            st.write("Copy the Timestamp description and add it to the Youtube Video Description")
            st.code(timestamps, language="")
        except Exception as e:
            st.error(str(e))
        finally:
            os.unlink(video_path)


# Utility function for selection and timestamp generation for existing videos
def select_existing_video():

    try:
        existing_videos = fetch_existing_videos()
        video_options = {f"{video['metadata']['filename']} ({video['_id']})": video['_id'] for video in existing_videos}
        
        if video_options:
            selected_video = st.selectbox("Select a video:", list(video_options.keys()))
            video_id = video_options[selected_video]
            
            video_url = get_video_url(video_id)
            if video_url:
                st.markdown(f"### Selected Video: {selected_video}")
                st.components.v1.html(get_hls_player_html(video_url), height=600)
            
            if st.button("Generate Timestamps"):
                with st.spinner("Generating timestamps..."):
                    client = TwelveLabs(api_key=API_KEY)
                    timestamps, _ = generate_timestamps(client, video_id)
                st.subheader("YouTube Chapter Timestamps")
                st.write("Copy the Timestamp description and add it to the Youtube Video Description")
                st.code(timestamps, language="")
        else:
            st.warning("No existing videos found in the index.")
    except Exception as e:
        st.error(str(e))

def main():
 
    tab1, tab2 = st.tabs(["**Upload a new video**", "**Select an existing video**"])

    with tab1:
        upload_and_process_video()

    with tab2:
        select_existing_video()

if __name__ == "__main__":
    main()