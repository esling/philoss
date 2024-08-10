"""

 ~ ESP-32 // Micropython ~
 request.py : Generic definition for web request

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import urequests
import ujson

url = "http://worldtimeapi.org/api/timezone/America/New_York"

while True:
    # Perform HTTP GET request on a non-SSL web
    response = urequests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = ujson.loads(response.text)
        # Extract the "datetime" field for New York
        ny_datetime = data["datetime"]
        # Split the date and time components
        date_part, time_part = ny_datetime.split("T")
        # Get only the first two decimal places of the time
        time_part = time_part[:8]
        # Get the timezone
        timezone = data["timezone"]
        # Display the New York date and time on separate lines
        print("New York Date:")
        print(date_part)
        print("New York Time:")
        print(time_part)
        print("Timezone:")
        print(timezone)
        # Update the display
        oled.show()
    else:
        oled.text("Failed to get the time for New York!")
        # Update the display
        oled.show()