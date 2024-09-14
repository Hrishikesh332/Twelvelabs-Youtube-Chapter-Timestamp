import os
import requests
from moviepy.editor import VideoFileClip
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()


API_KEY = os.getenv("API_KEY")
INDEX_ID = os.getenv("INDEX_ID")

# Convert seconds to MM:SS format
def seconds_to_mmss(seconds):

    minutes, seconds = divmod(int(seconds), 60)
    return f"{minutes:02d}:{seconds:02d}"

# Utility function to Generate Highlights with Twelve Labs SDK
def generate_timestamps(client, video_id, start_time=0):

    try:
        gist = client.generate.summarize(video_id=video_id, type="chapter")
        chapter_text = "\n".join([f"{seconds_to_mmss(chapter.start + start_time)}-{chapter.chapter_title}" for chapter in gist.chapters])
        return chapter_text, gist.chapters[-1].start + start_time
    except Exception as e:
        raise Exception(f"An error occurred while generating timestamps: {str(e)}")


# Trim video using moviepy
def trim_video(input_path, output_path, start_time, end_time):

    with VideoFileClip(input_path) as video:
        new_video = video.subclip(start_time, end_time)
        new_video.write_videofile(output_path, codec="libx264", audio_codec="aac")


# Fetch existing videos using INDEX_ID
def fetch_existing_videos():
    
    url = f"https://api.twelvelabs.io/v1.2/indexes/{INDEX_ID}/videos?page=1&page_limit=10&sort_by=created_at&sort_option=desc"
    headers = {"accept": "application/json", "x-api-key": API_KEY, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['data']
    else:
        raise Exception(f"Failed to fetch videos: {response.text}")

# Get video URL from video_id in INDEX_ID
def get_video_url(video_id):

    url = f"https://api.twelvelabs.io/v1.2/indexes/{INDEX_ID}/videos/{video_id}"
    headers = {"accept": "application/json", "x-api-key": API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['hls']['video_url'] if 'hls' in data and 'video_url' in data['hls'] else None
    else:
        raise Exception(f"Failed to get video URL: {response.text}")

# Process video (upload, trim if necessary, and generate timestamps)
def process_video(client, video_path, video_type):
  
    with VideoFileClip(video_path) as clip:
        duration = clip.duration

    if duration > 3600:
        raise Exception("Video duration exceeds 1 hour, Please upload a shorter video.")

    if video_type == "Basic Video (less than 30 mins)":
        task = client.task.create(index_id=INDEX_ID, file=video_path)
        task.wait_for_done(sleep_interval=5)
        if task.status == "ready":
            return generate_timestamps(client, task.video_id)
        else:
            raise Exception(f"Indexing failed with status {task.status}")
    
    elif video_type == "Podcast (30 mins to 1 hour)":
        # Process first 30 minutes
        trimmed_path = os.path.join(os.path.dirname(video_path), "trimmed_1.mp4")
        trim_video(video_path, trimmed_path, 0, 1800)
        task1 = client.task.create(index_id=INDEX_ID, file=trimmed_path)
        task1.wait_for_done(sleep_interval=5)
        os.remove(trimmed_path)
        if task1.status != "ready":
            raise Exception(f"Indexing failed with status {task1.status}")
        
        timestamps, end_time = generate_timestamps(client, task1.video_id)
        
        # Process remaining duration if video is longer than 30 minutes
        if duration > 1800:
            trimmed_path = os.path.join(os.path.dirname(video_path), "trimmed_2.mp4")
            trim_video(video_path, trimmed_path, 1800, int(duration))
            task2 = client.task.create(index_id=INDEX_ID, file=trimmed_path)
            task2.wait_for_done(sleep_interval=5)
            os.remove(trimmed_path)
            if task2.status != "ready":
                raise Exception(f"Indexing failed with status {task2.status}")
            
            timestamps_2, _ = generate_timestamps(client, task2.video_id, start_time=end_time)
            timestamps += "\n" + timestamps_2
        
        return timestamps


# HTML for the HLS video player
def get_hls_player_html(video_url):

    return f"""
    <script src="https://cdn.jsdelivr.net/npm/hls.js@latest"></script>
    <style>
        #video-container {{
            position: relative;
            width: 100%;
            padding-bottom: 56.25%; /* 16:9 Aspect Ratio */
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        #video {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
    </style>
    <div id="video-container">
        <video id="video" controls></video>
    </div>
    <script>
        var video = document.getElementById('video');
        var videoSrc = "{video_url}";
        if (Hls.isSupported()) {{
            var hls = new Hls();
            hls.loadSource(videoSrc);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function() {{
                video.pause();
            }});
        }}
        else if (video.canPlayType('application/vnd.apple.mpegurl')) {{
            video.src = videoSrc;
            video.addEventListener('loadedmetadata', function() {{
                video.pause();
            }});
        }}
    </script>
    """