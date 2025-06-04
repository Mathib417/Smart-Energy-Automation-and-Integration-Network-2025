import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix

import os, time
from influxdb_client_3 import InfluxDBClient3, Point
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

# InfluxDB Configuration
INFLUXDB_TOKEN = "kBLLkVYJr_s0oz0bqfnZDFk8AH-Kp8P56uwqWeZWfgJs7WV1HfHknQpyDMiXJbsqaReU_AOxtdq2MB6_sFol7w=="
token = INFLUXDB_TOKEN
org = "Dyson Sphere"
host = "https://us-east-1-1.aws.cloud2.influxdata.com"
database = "Bucket1"

client = InfluxDBClient3(host=host, token=token, org=org)
query_client = InfluxDBClient(url=host, token=token, org=org)

# Step 1: Create a sample dataset
data = {
    'Voltage': [200, 201, 198, 200, 201.2, 202, 199.5, 200.43],
    'Frequency': [50, 60, 70, 55, 65, 75, 53, 63],
    'OutputVoltageLevel': ['220V', '230V', '240V', '220V', '230V', '240V', '220V', '230V']
}
df = pd.DataFrame(data)

# Step 2: Preprocessing
X = df[['Voltage', 'Frequency']]
y = df['OutputVoltageLevel']

label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Step 3: Train-test split
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_encoded, test_size=0.2, random_state=42)

# Step 4: Train the model
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# Step 5: Evaluate the model
y_pred = clf.predict(X_test)

y_test_decoded = label_encoder.inverse_transform(y_test)
y_pred_decoded = label_encoder.inverse_transform(y_pred)

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test_decoded, y_pred_decoded))

# Step 6: Predict new values



query = f"""
from(bucket: "{database}")
  |> range(start: -1h)
  |> filter(fn: (r) => r["_measurement"] == "Inverters")
  |> filter(fn: (r) => r["_field"] == "Voltage")
  |> last()
"""
influx_data = []
predicted_voltage = []
try:
    tables = query_client.query_api().query(query)
    print(tables)
    for table in tables:
        count = 0
        for record in table.records:
            print(f"reading --> Time: {record.get_time()}, Voltage: {record.get_value()}")
            influx_data.append(record.get_value())
            new_data = [[influx_data[count], 50]]  # Example input
            new_data_scaled = scaler.transform(new_data)
            predicted_class = clf.predict(new_data_scaled)
            predicted_voltage.append(label_encoder.inverse_transform(predicted_class))
            count += 1
except Exception as e:
    print(f"Error querying data: {e}")

predicted_data = {
    "point1": {
        "Inverter_ID": "1",
        "Measurement": "Voltage",
        "Value": predicted_voltage[0],
    },
    "point2": {
        "Inverter_ID": "2",
        "Measurement": "Voltage",
        "Value": predicted_voltage[1],
    },
    "point3": {
        "Inverter_ID": "3",
        "Measurement": "Voltage",
        "Value": predicted_voltage[2],
    },
        "point4": {
        "Inverter_ID": "4",
        "Measurement": "Voltage",
        "Value": predicted_voltage[3],
    }
}

# Writing Data to InfluxDB
# for key in predicted_data:
#     point = (
#         Point("ML")
#         .tag("Inverter_ID", predicted_data[key]["Inverter_ID"])
#         .field(predicted_data[key]["Measurement"], predicted_data[key]["Value"])
#     )
#     client.write(database=database, record=point)
#     time.sleep(1)

# print("Data Written to InfluxDB.")

for i in range(4):
    print(f" predicted value of inverter {(i+1)}: {predicted_voltage[i]}")


# Reading Data from InfluxDB


query_client.close()
client.close()
print("Process Complete. Return to InfluxDB UI.")
