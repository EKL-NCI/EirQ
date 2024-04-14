# Erin's Code from raspberry pi
import time
from aq import AQ

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.exceptions import PubNubException
import uuid

sensorNo = '1'

aq = AQ()
aq.leds_automatic()

# Set up PubNub
# Note: Replace 'my_publish_key' and 'my_subscribe_key' with your actual PubNub keys
pnconfig = PNConfiguration()
pnconfig.publish_key = 'pub-c-719410fa-a675-4f72-8eae-5f71f0a938b5'
pnconfig.subscribe_key = 'sub-c-6afc2464-b330-469f-a68d-52cbba8aecc4'
pnconfig.ssl = True
pnconfig.uuid = str(uuid.uuid4())  # Generate a unique UUID for this client

pubnub = PubNub(pnconfig)
channel_name = 'aq_channel'  # The channel you want to publish to

def publish_callback(result, status):
    # Handle publish response and errors
    if not status.is_error():
        print("Publish success")
    else:
        print("Publish failed with status: ", status)


interval = int(input("Enter interval between readings (seconds):"))
file_name = input("Enter filename:")

auto_cal = input("Auto-calibrate at 2:00 AM (Y/N)?")

current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("Logging started at: " + current_time)
print("Press CTRL-c to end logging")

f = open(file_name, "w")
f.write("time(s)\ttemp(C)\teCO2(ppm)\t\tdateTime\tsensorNo\n")
print("time(s)\ttemp(C)\teCO2(ppm)\t\tdateTime\tsensorNo")

last_update = 0
t0 = int(time.monotonic())

warning_level = 0

try:
    while True:
        now = time.monotonic()
        if now > last_update + interval:
            last_update = now
            t = str(int(now) - t0)
            temp_c = str(aq.get_temp())
            eco2 = str(int(aq.get_eco2()))
            eco2_measure =int(aq.get_eco2())
            # Write to file
            f.write(t + "\t")
            f.write(temp_c + "\t")
            f.write(eco2 + "\n")
            current_time1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(t + "\t" + temp_c + "\t" + str(int(eco2))+ "\t" + current_time1 + "\t" + sensorNo)
    
            if(eco2_measure > 800):
                warning_level = 1
                data = {
                    'timestamp':t,
                    'temperature':temp_c,
                    'eCO2':eco2,
                    'current_time1':current_time1,
                    'sensorNo':sensorNo,
                    'warning_level':warning_level
                        }
                print("PubNubb", data )
            else:
                warning_level = 0
                data = {
                        'timestamp':t,
                        'temperature':temp_c,
                        'eCO2':eco2,
                        'current_time1':current_time1,
                        'sensorNo':sensorNo,
                        'warning_level':warning_level
                        }
                print("pubnub", data)

          


                  
            try:
                pubnub.publish().channel(channel_name).message(data).sync()
            except PubNubException as e:
                print("Failed to publish data to PubNub:", str(e))

        tm = time.localtime()
        if auto_cal.upper() == 'Y' and tm.tm_hour == 2 and tm.tm_min == 0 and tm.tm_sec == 0:
            print("recalibrating")
            aq.calibrate_400()
            time.sleep(1000)

except KeyboardInterrupt:
    f.close()
    print("\nLogging to file " + file_name + " complete")
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Logging ended at: " + current_time)

# End of Erin's code from raspberry pi
