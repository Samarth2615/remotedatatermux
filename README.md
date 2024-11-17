pkg update && pkg upgrade

pkg install termux-api

termux-setup-storage



pip install flask 



pkg install termux-api



pkg install python



install termux api app from https://f-droid.org/repo/com.termux.api_51.apk


install new termux from https://f-droid.org/repo/com.termux_1020.apk



run by python server.py



ssh-keygen for serveo

termux-wake-lock



pkg update && pkg upgrade -y && pkg install python termux-api git -y && termux-setup-storage && pip install flask






nohup ssh -o ServerAliveInterval=60 -R rudra:80:localhost:8080 serveo.net 





nohup python server.py &



pkg install termux-boot




mkdir -p ~/.termux/boot/
nano ~/.termux/boot/startup.sh




#!/data/data/com.termux/files/usr/bin/bash

# Prevent device from sleeping
termux-wake-lock

# Start localhost server
nohup python3 -m http.server 8080 &

# Start Serveo tunnel
nohup ssh -o ServerAliveInterval=60 -R rudra:80:localhost:8080 serveo.net &






# then
chmod +x ~/.termux/boot/startup.sh
Termux Server Setup with Serveo

This guide walks you through setting up a Python server on Termux and using Serveo for external access.

Table of Contents

1. Prerequisites


2. Installation

Update and Upgrade Packages

Install Required Packages

Termux Storage Setup

Install Flask



3. Running the Server


4. Setting Up Serveo Tunnel


5. Enable Termux Wake Lock


6. Auto Start on Boot


7. License




---

Prerequisites

Before you begin, make sure you have:

Termux API App: Download here

Latest Termux App: Download here



---

Installation

Update and Upgrade Packages

Open Termux and run:

pkg update && pkg upgrade -y

Install Required Packages

Install essential packages:

pkg install python termux-api git -y

Termux Storage Setup

Grant Termux access to device storage:

termux-setup-storage

Install Flask

Install Flask for running the Python server:

pip install flask


---

Running the Server

1. Create a server.py file with your Flask code. For example:

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


2. To start the Flask server, run:

python server.py




---

Setting Up Serveo Tunnel

To make your local server accessible over the internet:

nohup ssh -o ServerAliveInterval=60 -R 80:localhost:8080 serveo.net &
nohup python server.py &

The above command forwards external requests on port 80 to your local server on port 8080.



---

Enable Termux Wake Lock

Prevent your device from sleeping while the server is running:

termux-wake-lock


---

Auto Start on Boot

To automatically start your server and tunnel after reboot:

Step 1: Install Termux Boot

pkg install termux-boot

Step 2: Create a Startup Script

1. Create the directory if it doesn’t exist:

mkdir -p ~/.termux/boot/


2. Create the startup script:

nano ~/.termux/boot/startup.sh


3. Add the following content to startup.sh:

#!/data/data/com.termux/files/usr/bin/bash

# Prevent device from sleeping
termux-wake-lock

# Start the Flask server
nohup python3 -m http.server 8080 &

# Start Serveo tunnel
nohup ssh -o ServerAliveInterval=60 -R rudra:80:localhost:8080 serveo.net &


4. Save and exit (Ctrl + X, then Y, then Enter).


5. Make the script executable:

chmod +x ~/.termux/boot/startup.sh



Now, every time your device reboots, Termux will automatically start your server and Serveo tunnel.


---

License

This project is licensed under the MIT License - see the LICENSE file for details.


---

Feel free to copy this entire README into your GitHub repository!

