import os
import time
import glob
import ftplib
import paho.mqtt.client as mqtt
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

load_dotenv()

# This username is static and doesn't change between printers
FTP_USERNAME = "bblp"

# Connect to the FTP server
ftp  = ftplib.FTP(FTP_SERVER)
ftp.login(FTP_USERNAME, FTP_PASSWORD)

## Connect to the MQTT server
mqtt_client = mqtt.Client()
# This is just a place holder in the event that Bambu changes how MQTT works locally
# mqtt_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
mqtt_client.connect(MQTT_SERVER)

class FileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Find all .3mf files in the directory to monitor
        files = glob.glob(os.path.join(DIRECTORY_TO_MONITOR, "*.3mf"))
        
        # Upload each file to the FTP server
        for file in files:
            with open(file, "rb") as f:
                filename = os.path.split(file)[1]
                ftp.storbinary("STOR " + filename, f)
                print("Uploaded the file: " + filename)

        # Move the uploaded files to the "uploaded" directory
        for file in files:
            filename = os.path.split(file)[1]
            os.rename(file, os.path.join(UPLOADED_FILES_DIRECTORY, os.path.basename(file)))
            print("Moved the file: " + filename)
            # Send the MQTT Print command
            mqtt_client.publish("device/"+ DEV_ID +"/request", "{\"print\":{\"sequence_id\":0,\"command\":\"project_file\",\"param\":\"Metadata/plate_1.gcode\",\"subtask_name\":\""+ filename +"\",\"url\":\"ftp://"+ filename +"\",\"timelapse\":false,\"bed_leveling\":false,\"flow_cali\":false,\"vibration_cali\":false,\"layer_inspect\":true,\"use_ams\":true}}")
            print("Sent a \"Print Start\" notification for: " + filename)



# Create an observer and an event handler
observer = Observer()
event_handler = FileHandler()

# Monitor the directory for changes and start the observer
observer.schedule(event_handler, DIRECTORY_TO_MONITOR, recursive=True)
observer.start()

# Sleep until the observer is stopped
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()

observer.join()