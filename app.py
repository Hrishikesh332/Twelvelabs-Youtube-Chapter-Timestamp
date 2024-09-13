import streamlit as st
import tempfile
import os
import requests
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()

API_KEY = os.getenv("API_KEY")
INDEX_ID = os.getenv("INDEX_ID")

# Set up Streamlit page configuration
st.set_page_config(page_title="YouTube Chapter Timestamp Generator", layout="wide")

# Apply custom CSS for background and styling
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

# Display the title
st.markdown("<h2 style='text-align: center;'>YouTube Chapter Timestamp Generator ✍</h1>", unsafe_allow_html=True)
st.markdown("---")

# Utility function to convert seconds to MM:SS format
def seconds_to_mmss(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

# Utility callback function to update task status
def on_task_update(task: Task):
    st.text(f"Status: {task.status}")

# Utility function to fetch existing videos from the API
def fetch_existing_videos():
    url = f"https://api.twelvelabs.io/v1.2/indexes/{INDEX_ID}/videos?page=1&page_limit=10&sort_by=created_at&sort_option=desc"
    headers = {
        "accept": "application/json",
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        st.error(f"Failed to fetch videos: {response.text}")
        return []

# Utility function to generate timestamps for a given video ID
def generate_timestamps(video_id):
    try:
        client = TwelveLabs(api_key=API_KEY)
        with st.spinner("Generating chapters..."):
            gist = client.generate.summarize(video_id=video_id, type="chapter")

        st.subheader("YouTube Chapter Timestamps")
        chapter_text = ""
        for chapter in gist.chapters:
            time_formatted = seconds_to_mmss(chapter.start)
            chapter_line = f"{time_formatted}-{chapter.chapter_title}"
            chapter_text += chapter_line + "\n"
        
        st.write("Copy the Timestamp description and add it to the Youtube Video Description")
        st.code(chapter_text, language="")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Main function
def main():
    # Tabs for different options
    tab1, tab2 = st.tabs(["**Upload a new video**", "**Select an existing video**"])

    with tab1:
        uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

        if uploaded_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
                tmp_file.write(uploaded_file.read())
                video_path = tmp_file.name

            try:
                client = TwelveLabs(api_key=API_KEY)
                with st.spinner("Creating task..."):
                    task = client.task.create(index_id=INDEX_ID, file=video_path)
                    st.success(f"Task created: id={task.id}")

                with st.spinner("Processing video..."):
                    task.wait_for_done(sleep_interval=5, callback=on_task_update)
                    if task.status != "ready":
                        st.error(f"Indexing failed with status {task.status}")
                    else:
                        st.success(f"Video processed successfully. Video ID: {task.video_id}")
                        generate_timestamps(task.video_id)

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                os.unlink(video_path)

    with tab2:
        existing_videos = fetch_existing_videos()
        video_options = {f"{video['metadata']['filename']} ({video['_id']})": video['_id'] for video in existing_videos}
        selected_video = st.selectbox("Select a video:", list(video_options.keys()))
        video_id = video_options[selected_video]

        if st.button("Generate Timestamps"):
            generate_timestamps(video_id)

if __name__ == "__main__":
    main()