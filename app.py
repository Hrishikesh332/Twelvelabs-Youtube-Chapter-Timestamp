import streamlit as st
import tempfile
import os
from twelvelabs import TwelveLabs
from utils import (
    API_KEY, process_video, fetch_existing_videos,
    get_video_url, get_hls_player_html, generate_timestamps,
    download_video_segment, create_video_segments
)
import uuid 

# Set up the Streamlit page configuration
st.set_page_config(page_title="YouTube Chapter Timestamp Generator", layout="wide")

# Custom CSS
st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://cdn.pixabay.com/photo/2021/08/02/22/41/background-6517956_640.jpg");
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

# Streamlit Page Header
st.markdown("<h2 style='text-align: center;'>YouTube Chapter Timestamp Generator ✍</h2>", unsafe_allow_html=True)
st.markdown("---")

# Initialize session state
if 'timestamps' not in st.session_state:
    st.session_state.timestamps = None
if 'video_id' not in st.session_state:
    st.session_state.video_id = None
if 'video_segments' not in st.session_state:
    st.session_state.video_segments = []
if 'video_url' not in st.session_state:
    st.session_state.video_url = None


# Function to Display the Segment and also Download
def display_segment(file_name, description, segment_index):
    if os.path.exists(file_name):
        st.write(f"### {description}")
        st.video(file_name)
        with open(file_name, "rb") as file:
            file_contents = file.read()
        unique_key = f"download_{segment_index}_{uuid.uuid4()}"
        st.download_button(
            label=f"Download: {description}",
            data=file_contents,
            file_name=file_name,
            mime="video/mp4",
            key=unique_key
        )
        st.markdown("---")
    else:
        st.warning(f"File {file_name} not found. It may have been deleted or moved.")


# Function to process the segment
def process_and_display_segments():
    if not st.session_state.video_url:
        st.error("Video URL not found. Please reprocess the video.")
        return

    segment_generator = create_video_segments(st.session_state.video_url, st.session_state.timestamps)

    progress_bar = st.progress(0)
    status_text = st.empty()

    st.session_state.video_segments = []  # Reset video segments
    total_segments = len(st.session_state.timestamps.split('\n'))

    for i, (file_name, description) in enumerate(segment_generator, 1):
        st.session_state.video_segments.append((file_name, description))
        display_segment(file_name, description, i-1)  # Pass the index here
        progress = i / total_segments
        progress_bar.progress(progress)
        status_text.text(f"Processing segment {i}/{total_segments}...")

    progress_bar.progress(1.0)
    status_text.text("All segments processed!")


# Uplaoding feature and the processing of the video
def upload_and_process_video():
    video_type = st.selectbox("Select video type:", ["Basic Video (less than 30 mins)", "Podcast (30 mins to 1 hour)"])
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file and st.button("Process Video", key="process_video_button"):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name
        try:
            with st.spinner("Processing video..."):
                client = TwelveLabs(api_key=API_KEY)
                timestamps, video_id = process_video(client, video_path, video_type)
            st.success("Video processed successfully!")
            st.session_state.timestamps = timestamps
            st.session_state.video_id = video_id
            st.session_state.video_url = get_video_url(video_id)
            if st.session_state.video_url:
                st.video(st.session_state.video_url)
            else:
                st.error("Failed to retrieve video URL.")
        except Exception as e:
            st.error(str(e))
        finally:
            os.unlink(video_path)

# Selecting the existing video from the Index and generating timestamps highlight
def select_existing_video():
    try:
        existing_videos = fetch_existing_videos()
        video_options = {f"{video['metadata']['filename']} ({video['_id']})": video['_id'] for video in existing_videos}
        
        if video_options:
            selected_video = st.selectbox("Select a video:", list(video_options.keys()))
            video_id = video_options[selected_video]
            
            st.session_state.video_id = video_id
            st.session_state.video_url = get_video_url(video_id)
            
            if st.session_state.video_url:
                st.markdown(f"### Selected Video: {selected_video}")
                st.video(st.session_state.video_url)
            else:
                st.error("Failed to retrieve video URL.")
            
            if st.button("Generate Timestamps", key="generate_timestamps_button"):
                with st.spinner("Generating timestamps..."):
                    client = TwelveLabs(api_key=API_KEY)
                    timestamps, _ = generate_timestamps(client, video_id)
                st.session_state.timestamps = timestamps
        else:
            st.warning("No existing videos found in the index.")
    except Exception as e:
        st.error(str(e))


# Function to display the timestamps and the segments
def display_timestamps_and_segments():
    if st.session_state.timestamps:
        st.subheader("YouTube Chapter Timestamps")
        st.write("Copy the Timestamp description and add it to the Youtube Video Description")
        st.code(st.session_state.timestamps, language="")

        if st.button("Create Video Segments", key="create_segments_button"):
            try:
                process_and_display_segments()
            except Exception as e:
                st.error(f"Error creating video segments: {str(e)}")
                st.exception(e)  # This will display the full traceback

        if st.session_state.video_segments:
            st.subheader("Video Segments")
            for index, (file_name, description) in enumerate(st.session_state.video_segments):
                display_segment(file_name, description, index)

            if st.button("Clear all segments", key="clear_segments_button"):
                for file_name, _ in st.session_state.video_segments:
                    if os.path.exists(file_name):
                        os.remove(file_name)
                st.session_state.video_segments = []
                st.success("All segment files have been cleared.")
                st.experimental_rerun()

def main():
    tab1, tab2 = st.tabs(["**Upload a new video**", "**Select an existing video**"])

    with tab1:
        upload_and_process_video()

    with tab2:
        select_existing_video()

    display_timestamps_and_segments()

if __name__ == "__main__":
    main()