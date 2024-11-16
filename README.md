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






nohup ssh -o ServerAliveInterval=60 -R 80:localhost:8080 serveo.net &
nohup python server.py &



pkg install termux-boot


chmod +x ~/.termux/boot/startup.sh

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
