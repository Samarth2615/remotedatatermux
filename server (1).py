from flask import Flask, jsonify, request, send_file, render_template_string
import os
import json

app = Flask(__name__)

# Helper function to run Termux commands
def run_termux_command(command):
    result = os.popen(command).read()
    try:
        return json.loads(result)
    except:
        return result

# Serve the HTML page
@app.route('/')
def home():
    return render_template_string(open('index.html').read())

# Route to read the 10 latest SMS messages
@app.route('/read_sms', methods=['GET'])
def read_sms():
    return jsonify(run_termux_command("termux-sms-list -l 10"))

# Route to send SMS
@app.route('/send_sms', methods=['POST'])
def send_sms():
    number = request.form.get('number')
    message = request.form.get('message')
    if number and message:
        os.system(f"termux-sms-send -n {number} {message}")
        return jsonify({"status": "SMS sent"})
    return jsonify({"error": "Number and message required"}), 400

# Route to make a phone call
@app.route('/make_call', methods=['POST'])
def make_call():
    number = request.form.get('number')
    if number:
        os.system(f"termux-telephony-call {number}")
        return jsonify({"status": f"Calling {number}"})
    return jsonify({"error": "Phone number required"}), 400

# Route to access contacts
@app.route('/get_contacts', methods=['GET'])
def get_contacts():
    contacts = run_termux_command("termux-contact-list")
    return jsonify(contacts)

# Route to get call logs
@app.route('/get_call_logs', methods=['GET'])
def get_call_logs():
    logs = run_termux_command("termux-call-log")
    return jsonify(logs)

# Optimized Photo Capture (Deletes photo after sending)
@app.route('/capture_photo', methods=['GET'])
def capture_photo():
    camera_id = request.args.get('camera', '0')
    photo_path = "/data/data/com.termux/files/home/temp_photo.jpg"
    os.system(f"termux-camera-photo -c {camera_id} {photo_path}")
    if os.path.exists(photo_path):
        with open(photo_path, 'rb') as f:
            photo_data = f.read()
        os.remove(photo_path)  # Ensure the photo is deleted after use
        return photo_data, 200, {'Content-Type': 'image/jpeg'}
    return jsonify({"error": "Failed to capture photo"}), 500

# Route for file browsing
def list_files(path):
    try:
        items = []
        for entry in os.scandir(path):
            items.append({
                'name': entry.name,
                'path': entry.path,
                'is_dir': entry.is_dir()
            })
        return items
    except FileNotFoundError:
        return []

@app.route('/browse', methods=['GET'])
def browse():
    path = request.args.get('path', '/sdcard')
    items = list_files(path)
    current_path = os.path.abspath(path)
    parent_path = os.path.dirname(current_path)
    return render_template_string("""
        <h2>File Browser</h2>
        <p>Current Path: {{ current_path }}</p>
        <a href="/browse?path={{ parent_path }}">Up</a>
        <ul>
            {% for item in items %}
                <li>
                    {% if item.is_dir %}
                        <a href="/browse?path={{ item.path }}">{{ item.name }}/</a>
                    {% else %}
                        {{ item.name }} - 
                        <a href="/download?path={{ item.path }}">Download</a> | 
                        <a href="/delete?path={{ item.path }}">Delete</a>
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    """, items=items, current_path=current_path, parent_path=parent_path)

@app.route('/download', methods=['GET'])
def download():
    file_path = request.args.get('path')
    if file_path and os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "File not found"}), 404

@app.route('/delete', methods=['GET'])
def delete():
    file_path = request.args.get('path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
        return redirect(f"/browse?path={os.path.dirname(file_path)}")
    return jsonify({"error": "File not found"}), 404
# Show a system notification
@app.route('/show_notification', methods=['POST'])
def show_notification():
    title = request.form.get('title', 'Notification')
    content = request.form.get('content', 'This is a test notification.')
    os.system(f"termux-notification --title '{title}' --content '{content}'")
    return jsonify({"status": "Notification sent"})

# Control the torch (on/off)
@app.route('/torch', methods=['POST'])
def control_torch():
    state = request.form.get('state')
    if state == 'on':
        os.system("termux-torch on")
    elif state == 'off':
        os.system("termux-torch off")
    else:
        return jsonify({"error": "Invalid state"}), 400
    return jsonify({"status": f"Torch turned {state}"})

# Change system volume
@app.route('/change_volume', methods=['POST'])
def change_volume():
    volume_type = request.form.get('type', 'media')
    level = request.form.get('level', 5)  # Default level 5
    os.system(f"termux-volume {volume_type} {level}")
    return jsonify({"status": f"{volume_type} volume set to {level}"})

# Speak text using TTS
@app.route('/speak_text', methods=['POST'])
def speak_text():
    text = request.form.get('text')
    if text:
        os.system(f"termux-tts-speak '{text}'")
        return jsonify({"status": "Text spoken"})
    return jsonify({"error": "No text provided"}), 400

# New Feature: Vibrate the device
@app.route('/vibrate', methods=['POST'])
def vibrate():
    duration = request.form.get('duration', '500')
    os.system(f"termux-vibrate -d {duration}")
    return jsonify({"status": f"Vibrated for {duration}ms"})

# New Feature: Modify System Settings (Wi-Fi, Bluetooth, Brightness)
@app.route('/modify_settings', methods=['POST'])
def modify_settings():
    setting = request.form.get('setting')
    value = request.form.get('value')
    
    if setting == 'wifi':
        os.system(f"termux-wifi-{value}")  # value should be 'enable' or 'disable'
        return jsonify({"status": f"Wi-Fi {value}d"})
    
    elif setting == 'bluetooth':
        os.system(f"termux-bluetooth-{value}")  # value should be 'on' or 'off'
        return jsonify({"status": f"Bluetooth turned {value}"})
    
    elif setting == 'brightness':
        os.system(f"termux-brightness {value}")  # value should be a number between 0 and 255
        return jsonify({"status": f"Brightness set to {value}"})
    
    return jsonify({"error": "Invalid setting or value"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)