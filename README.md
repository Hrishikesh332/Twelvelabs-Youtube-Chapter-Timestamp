<br />
<div align="center">
  <h3 align="center">YouTube Chapter Highlight Generator</h3>
  <p align="center">
    Generate chapter highlight timestamps for YouTube videos
    <br />
    <a href="https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://twelvelabs-highlight-generator.streamlit.app/">View Demo</a>
    ·
    <a href="https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp/issues">Report Bug</a>
    ·
    <a href="https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp/issues">Request Feature</a>
  </p>
</div>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about">About</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#tech-stack">Tech Stack</a></li>
    <li><a href="#instructions-on-running-project-locally">Instructions on running project locally</a></li>
    <li><a href="#usecases">Usecases</a></li>
    <li><a href="#feedback">Feedback</a></li>
  </ol>
</details>

------

## About

The YouTube Chapter Highlight Generator is a tool developed to automatically generate chapter timestamps for YouTube videos. By analyzing the video's content, it identifies key segments and creates timestamps that can be used to create chapters for better video navigation and user experience.

It focuses on solving the problem of the content creator by saving the time and the efforts. The snippet of the Timestamp higlight generated can be pasted for that video in the youtube description of that video, which directly implements the chapter highlights.

There are two segments features, Basic video (Less than 30 mins) and the Podcast (more than 30 mins). 

## Demonstration

Try the Application Now -

<a href="https://twelvelabs-highlight-generator.streamlit.app/" target="_blank" style="
    display: inline-block;
    padding: 12px 24px;
    font-size: 18px;
    font-weight: bold;
    color: #ffffff;
    background-color: #007bff;
    border: none;
    border-radius: 8px;
    text-align: center;
    text-decoration: none;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    transition: background-color 0.3s, box-shadow 0.3s;
">
    YouTube Chapter Timestamp App
</a>


Demo and Video Explanation -


  [![Watch the video](https://img.youtube.com/vi/z-_PJqjTZmM/hqdefault.jpg)](https://youtu.be/z-_PJqjTZmM)

## Features

🎯 **Chapter Generation**: Automatically detect and create timestamps with highlights for video chapters.

🔍 **Content Segmentation**: Identify key points in the video based on its content.

🚀 **Streamlined Navigation**: Enhance the viewing experience with clickable chapters for easier navigation.

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **Deployment**: Streamlit Cloud


## Flow Breakdown

![https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp/blob/main/src/flow.png](https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp/blob/main/src/flow.png)

## Instructions on running project locally

To run the YouTube Chapter Highlight Generator locally, follow these steps -

### Step 1 - Clone the project

```bash
git clone https://github.com/Hrishikesh332/Twelvelabs-Youtube-Chapter-Timestamp.git


Step 2  -

Install dependencies:

```bash
 cd Youtube-Chapter-Timestamp-App
 
 pip install -r requirements.txt
```

Step 3 - 

Set up your Twelve Labs account -

Create an account on the Twelve Labs Portal
Navigate to the Twelve Labs Playground
Create a new index, select Marengo 2.6 and Pegasus 1.1


Step 4 -

Get your API Key from the [Twelve Labs Dashboard](https://playground.twelvelabs.io/dashboard/api-key)
Find your INDEX_ID in the URL of your created [index](https://playground.twelvelabs.io/indexes/{index_id})

Step 5 -

Configure the application with your API credentials.

Step 6 -

Run the Streamlit application

```bash
  streamlit run app.py
```

Step 7 - 

Run the Server -

```bash
  http://localhost:8501/
```

## Usecases

📽️**YouTube Content Creators**: Automatically generate chapter highlight markers for improved video navigation.

🎓 **Educational Videos**: Make it easier for students to jump to specific sections of long tutorial videos.

🎥 **Content Review**: Easily navigate to important points in long-form video content.

## Feedback

If you have any feedback, please reach out to us at **hriskikesh.yadav332@gmail.com**


## License

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


