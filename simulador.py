import time
import random
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Configuración
token = "vpxPgpJF_vyWlMouNxHDOL3GsGsX53hRHnijI028JLHkLcl3DT879TeFK22aH2BnGmczbvrlT59YrGN12btamw=="
org = "Universidad de Sevilla"
bucket = "sensores_raw"
url = "http://localhost:8086"

client = InfluxDBClient(url=url, token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)

print("Iniciando envío de datos...")

try:
    while True:
        for sensor_id in ["sensor_A", "sensor_B"]:
            
            temp = random.uniform(20.0, 25.0)
            hum = random.uniform(40.0, 60.0)
            
            point = Point("lectura_clima") \
                .tag("sensor", sensor_id) \
                .tag("aula", "Lab_1") \
                .field("temperatura", temp) \
                .field("humedad", hum)
            
            write_api.write(bucket=bucket, org=org, record=point)
            print(f"Enviado: {sensor_id} -> Temp: {temp:.2f}")
        
        time.sleep(1)
except KeyboardInterrupt:
    print("Simulación detenida.")