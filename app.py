import os
import subprocess
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
STATIC_FOLDER = 'static/'
TEMPLATES_FOLDER = 'templates/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads and static directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)
os.makedirs(TEMPLATES_FOLDER, exist_ok=True)

def init_directories(src_dir = "./app/"):
    try:
        for filename in os.listdir(src_dir):
            src_file = os.path.join(src_dir, filename)
            if filename.endswith(".html"):
                dest_file = os.path.join("./templates/", filename)
            else:
                dest_file = os.path.join("./static/", filename)
            # If it's a file, copy it
            if os.path.isfile(src_file):
                shutil.copy(src_file, dest_file)
    except Exception as e:
        print(f"An error occurred: {e}")

def detect_scenes(filepath, threshold):
    # Create a text file to store timecodes
    timecodes_file = os.path.join(UPLOAD_FOLDER, 'timecodes.txt')

    # FFmpeg command to detect scenes
    cmd = [
        'ffmpeg', '-i', filepath, '-vf', f"select='gt(scene,{threshold})',showinfo",
        '-f', 'null', '-'
    ]

    # Extract timecodes from FFmpeg log
    with open(timecodes_file, 'w') as f:
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
        _, err = process.communicate()
        err_lines = err.decode('utf-8').split('\n')
        for line in err_lines:
            if "pts_time" in line:
                time_index = line.find('pts_time:')
                timecode = line[time_index + 9:].split()[0]
                f.write(timecode + '\n')

    return timecodes_file

def split_video(filepath, timecodes_file):
    # Get the original filename without extension
    original_filename = os.path.splitext(os.path.basename(filepath))[0]
    scene_count = 1
    scenes_list = []

    # Read timecodes from the file
    with open(timecodes_file, 'r') as f:
        timecodes = [float(line.strip()) for line in f.readlines()]

    # Include start time as the first scene
    timecodes.insert(0, 0.0)

    # Get the duration of the original video
    duration_cmd = [
        'ffprobe', '-v', 'error', '-show_entries',
        'format=duration', '-of',
        'default=noprint_wrappers=1:nokey=1', filepath
    ]
    video_duration = float(subprocess.check_output(duration_cmd).decode().strip())

    # Split videos based on detected timecodes
    for i in range(len(timecodes)):
        start_time = timecodes[i]
        # Calculate duration for the current scene
        if i + 1 < len(timecodes):
            duration = timecodes[i + 1] - start_time
        else:
            duration = video_duration - start_time
        if duration<=0.1 :
            continue
        # Generate output filename
        output_filename = f"{original_filename}_scene_{scene_count}.mp4"
        output_path = os.path.join(STATIC_FOLDER, output_filename)

        # FFmpeg command to extract scenes
        cmd = [
                'ffmpeg', '-y', '-i', filepath,
                '-ss', str(start_time), '-t', str(duration),
                '-c', 'copy', output_path
        ]
        subprocess.run(cmd)

        scenes_list.append(output_filename)
        scene_count += 1

    return scenes_list

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)

    file = request.files['file']
    threshold = request.form.get('threshold', 0.4)
    threshold = float(threshold)

    if file.filename == '':
        return redirect(request.url)

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Detect scenes and split video
        timecodes_file = detect_scenes(filepath, threshold)
        scenes = split_video(filepath, timecodes_file)

        return render_template('index.html', scenes=scenes)

def cleanup():
    try:
        if os.path.exists(UPLOAD_FOLDER):
            shutil.rmtree(UPLOAD_FOLDER)
        if os.path.exists(STATIC_FOLDER):
            shutil.rmtree(STATIC_FOLDER)
        if os.path.exists(TEMPLATES_FOLDER):
            shutil.rmtree(TEMPLATES_FOLDER)
    except Exception:
        pass

if __name__ == '__main__':
    init_directories()
    app.run(debug=True)
    cleanup()
