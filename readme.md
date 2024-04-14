# EirQ
## About Us
- EirQ aims to bring to the table an easy way for public transport systems and services to be able to track and monitor the air quality aboard their vehicles.​
- The system utilizes an air quality sensor connected to a raspberry pi, making implementation costs quite cheap for clients.
- EirQ makes use of a web application in order to display the live data collected from the sensor.
- The application allows users to view the temperature in the area of the sensor, and also the carbon dioxide levels in the air in parts per million.


## How to Run

### Flask Installation
```bash
 # Flask Installation
    pip install Flask
```

## Packages Needed
```bash
 # Packages needed (If VS code is used, may need to put py -m before installs)
    pip install pubnub
    pip install firebase_admin
    pip install pyrebase4
```


### How to run application once packages are installed
- 1. Navigate to app.py
- 2. Ensure pubnub and firebase credentials are correct
- 3. Run app.py 
- 4. If running in terminal use following command
```bash
    python app.py
```