import os
import subprocess
from flask import Flask, render_template_string, request, send_file

app = Flask(__name__)

# Function to switch between front and back camera
def capture_camera(front=True):
    try:
        print(f"Capturing {'front' if front else 'back'} camera...")
        camera_cmd = "termux-camera-photo -c 1 /sdcard/front_camera.jpg" if front else "termux-camera-photo -c 0 /sdcard/back_camera.jpg"
        
        os.system(camera_cmd)
        
        file_path = '/sdcard/front_camera.jpg' if front else '/sdcard/back_camera.jpg'
        if os.path.exists(file_path):
            return file_path
        else:
            print(f"Camera file not found for {'front' if front else 'back'} camera.")
            return None
    except Exception as e:
        print(f"Error during camera capture: {e}")
        return None

# Function to list files in a directory
def list_files(path):
    try:
        items = []
        for entry in os.scandir(path):
            items.append({'name': entry.name, 'path': entry.path, 'is_dir': entry.is_dir()})
        return items
    except FileNotFoundError:
        return []

# Route for file browsing
@app.route('/browse')
def browse():
    path = request.args.get('path', '/sdcard')
    items = list_files(path)
    return render_template_string(main_template, items=items, current_path=path)

# Route for downloading files
@app.route('/download')
def download():
    file_path = request.args.get('path')
    return send_file(file_path, as_attachment=True)

# Route for deleting files
@app.route('/delete')
def delete():
    file_path = request.args.get('path')
    if os.path.exists(file_path):
        os.remove(file_path)
    return redirect('/browse')

# Route for camera capture (front by default)
@app.route('/camera')
def camera():
    front = request.args.get('front', 'true') == 'true'
    file_path = capture_camera(front)
    if file_path:
        # Send the image file to the user
        response = send_file(file_path, mimetype='image/jpeg')
        # Delete the image from local storage after sending it
        os.remove(file_path)
        return response
    else:
        return "Error: Unable to capture camera", 500

# Updated HTML Template for the Web Interface
main_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Termux Web Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        button { padding: 10px; margin: 5px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background-color: #0056b3; }
        hr { margin: 20px 0; }
        img { max-width: 100%; height: auto; }
        audio { width: 100%; }
        ul { list-style-type: none; padding: 0; }
        li { margin: 5px 0; }
    </style>
</head>
<body>
    <h1>Termux Web Panel</h1>
    <button onclick="window.location.href='/camera?front=true'">Capture Front Camera</button>
    <button onclick="window.location.href='/camera?front=false'">Capture Back Camera</button>
    <hr>
    
    <h2>File Browser</h2>
    <p>Current Directory: {{ current_path }}</p>
    <ul>
        {% for item in items %}
        <li>
            {% if item.is_dir %}
                <a href="/browse?path={{ item.path }}">{{ item.name }}/</a>
            {% else %}
                <a href="/download?path={{ item.path }}">{{ item.name }}</a>
                <a href="/delete?path={{ item.path }}" style="color: red; margin-left: 10px;">[Delete]</a>
            {% endif %}
        </li>
        {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/')
def home():
    return '''
        <h1>Termux Web Panel</h1>
        <button onclick="window.location.href='/camera?front=true'">Front Camera</button>
        <button onclick="window.location.href='/camera?front=false'">Back Camera</button>
        <button onclick="window.location.href='/browse'">Browse Files</button>
    '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)