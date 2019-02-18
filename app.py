import Adafruit_DHT
import datetime
from influxdb import InfluxDBClient

if __name__ == "__main__":

    json_body = [
        {
            "measurement": "th",
            "tags": {},
            "time": datetime.datetime.now().isoformat(),
            "fields": {
                "temperature": None,
                "humidity": None,
            }
        }
    ]

    sensor = Adafruit_DHT.DHT11
    pin = 4

    client = InfluxDBClient('127.0.0.1', 8086, 'py', 'python', 'mydb')

    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

        json_body[0]['fields']['temperature'] = temperature
        json_body[0]['fields']['humidity'] = humidity
        json_body[0]['time'] = datetime.datetime.now().isoformat()

        print("Write points: {0}".format(json_body))
        client.write_points(json_body)

    else:
        print('Failed to get reading. Try again!')