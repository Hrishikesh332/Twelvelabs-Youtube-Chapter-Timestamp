import streamlit as st
import tempfile
import os
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task
from dotenv import load_dotenv

load_dotenv()


API_KEY = os.getenv("API_KEY")
INDEX_ID = os.getenv("INDEX_ID")


# Background Setting of the App
page_element = """
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
"""
st.markdown(page_element, unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center;'>YouTube Chapter Timestamp Generator ✍</h1>", unsafe_allow_html=True)
st.markdown("---")

# Utility function to convert seconds to MM:SS format
def seconds_to_mmss(seconds):
    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

# Utility function to print the status of a video indexing task
def on_task_update(task: Task):
    st.text(f"Status: {task.status}")

# Main Application
def main():

    # File uploader
    uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_file:
            tmp_file.write(uploaded_file.read())
            video_path = tmp_file.name

        try:
            # TwelveLabs Client Setup
            client = TwelveLabs(api_key=API_KEY)

            # Create task
            with st.spinner("Creating task..."):
                task = client.task.create(index_id=INDEX_ID, file=video_path)
                st.success(f"Task created: id={task.id}")

            # Wait for task to complete
            with st.spinner("Processing video..."):
                task.wait_for_done(sleep_interval=5, callback=on_task_update)
                if task.status != "ready":
                    st.error(f"Indexing failed with status {task.status}")
                else:
                    st.success(f"Video processed successfully. Video ID: {task.video_id}")

            # Generate summary
            with st.spinner("Generating chapters..."):
                gist = client.generate.summarize(video_id=task.video_id, type="chapter")

            # Format and display the results
            st.subheader("YouTube Chapter Timestamps")
            chapter_text = ""
            for chapter in gist.chapters:
                time_formatted = seconds_to_mmss(chapter.start)
                chapter_line = f"{time_formatted}-{chapter.chapter_title}"
                chapter_text += chapter_line + "\n"
                st.write(chapter_line)

            # The copy button with the st.code
            st.code(chapter_text, language="")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

        finally:
            # Clean up the temporary file
            os.unlink(video_path)

if __name__ == "__main__":
    main()