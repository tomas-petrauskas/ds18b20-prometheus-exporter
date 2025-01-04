from pathlib import Path
import time
from prometheus_client import start_http_server, Gauge
from DS18B20dvr.DS18B20 import DS18B20

def get_all_sensors():
    base_path = Path("/sys/bus/w1/devices/w1_bus_master1")
    master_slaves_path = base_path / "w1_master_slaves"

    try:
        sensor_ids = master_slaves_path.read_text().strip().split('\n')
        print(f"Slaves on this bus: {sensor_ids}")
        return sensor_ids
    except FileNotFoundError:
        print("Error: Could not find w1_master_slaves file. Is the 1-Wire bus configured correctly?")
        return []

def update_gauge(gauge, sensor_ids):
    for sensor_id in sensor_ids:
        _sensor = DS18B20(sensor_id)
        temp = _sensor.read_temperature()
        gauge.labels(device_id=sensor_id, hostname="local").set(temp)
        print(f"Updating {sensor_id} with {temp}")

device_ids = get_all_sensors()

if not device_ids:
    print("No DS18B20 sensors detected.")
    exit

    print(f"Found {len(device_ids)} sensor(s): {device_ids}")

gauge = Gauge(
        "onewire_temperature_c",
        "Temperature readings from DS18B20 sensors",
        ["device_id", "hostname"]
    )

if __name__ == '__main__':
    start_http_server(80)

    while True:
        update_gauge(gauge, device_ids)
        time.sleep(1)