# Installation Guide

This document provides step-by-step instructions for installing the **TekMedia's Video Scene Splitter**.

## Prerequisites

Before you begin, ensure you have met the following requirements:

Software:
- FFmpeg (version >= 5.0) installed
- Python (version >= 3.6) installed
	
Python Packages:
- Flask for building the web server
	
	 
## Installation Steps

1. **Clone the repository**:

```
git clone https://github.com/TekMedia-Software/Video-Scene-Splitter.git
```

2. **Navigate to the project directory**:

```
cd Video-Scene-Splitter
```

3. **Install dependencies**:
   
- If pip is not installed, you can install it using:

```
sudo apt install python3-pip
```
- Then, install the required Python packages:
```
pip install flask
```   	   
- Check if FFmpeg is installed correctly:
```
ffmpeg -version
```
- If FFmpeg is not installed, you can install it using:
```
sudo apt update
```
```
sudo apt install ffmpeg
```
- You can also download from [FFmpeg's official website](https://www.ffmpeg.org/download.html).

## Configuration

- Adjust the Scene Detection Threshold:
  - The default threshold value for scene detection is set in the UI.
  - You can modify it as per your requirements when running the application. 
- Supported Video Formats:
  - This project supports .mp4, .avi, .mov, .ts and .mkv video files.

## Running the Project

- To run the project after installation, use the following command:
```
python app.py
```
(or)
```
python3 app.py
```
- Now, open http://localhost:5000 in browser.

## Usage 

- How to Use
  - Upload a .mp4 or .ts video file.
  - Adjust the scene detection threshold if needed.
  - Click "Process" to split the video into scenes.
  - Download or play the split scenes from the provided links on the UI.


## Contact

If you encounter any issues or have questions regarding the installation, please contact:

- Awadh Bajpai - [awabaj@tekmediasoft.net](mailto:awabaj@tekmediasoft.net)
- Dhanya Saminathan - [dhasam@tekmediasoft.net](mailto:dhasam@tekmediasoft.net)

