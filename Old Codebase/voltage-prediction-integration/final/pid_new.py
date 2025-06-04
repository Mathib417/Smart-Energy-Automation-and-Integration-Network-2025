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
        for record in table.records:
            print(f"reading --> Time: {record.get_time()}, Voltage: {record.get_value()}")
            influx_data.append(record.get_value())
            
            
except Exception as e:
    print(f"Error querying data: {e}")



class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        self.setpoint = setpoint  # Desired voltage (230V)
        self.previous_error = 0
        self.integral = 0

    def compute(self, measured_value):
        # Calculate error
        error = self.setpoint - measured_value

        # Proportional term
        P = self.Kp * error

        # Integral term
        self.integral += error
        I = self.Ki * self.integral

        # Derivative term
        derivative = error - self.previous_error
        D = self.Kd * derivative

        # Save error for next iteration
        self.previous_error = error

        # Compute PID output
        output = P + I + D
        return output

def simulate_inverter(initial_voltage, target_voltage, Kp, Ki, Kd):
    
    
    


    # Initialize PID controller
    pid = PIDController(Kp, Ki, Kd, target_voltage)

    # Simulate the system
    current_voltage = initial_voltage
    time_step = 0.1  # Time step for simulation (in seconds)
    time_elapsed = 0

    print(f"Starting voltage: {current_voltage}V, Target voltage: {target_voltage}V")
    print("Time (s)\tVoltage (V)\tControl Signal")

    while abs(target_voltage - current_voltage) > 0.1:  # Stop when close to target
        
        
        predicted_voltage = [0]
        
        # Compute control signal using PID
        control_signal = pid.compute(current_voltage)

        # Simulate the effect of the control signal on the voltage
        # (This is a simple model; replace with your actual system dynamics)
        current_voltage += control_signal * time_step
        
        predicted_voltage[0] = int(current_voltage) 
        
        predicted_data = {
        "point1": {
        "Inverter_ID": "1",
        "Measurement": "voltage",
        "Value": predicted_voltage[0],
    }
        }
        
        for key in predicted_data:
            point = (
                Point("ML")
                .tag("Inverter_ID", predicted_data[key]["Inverter_ID"])
                .field(predicted_data[key]["Measurement"], predicted_data[key]["Value"])
                )
            client.write(database=database, record=point)
            time.sleep(1)

        print("Data Written to InfluxDB.")

        # Print results
        print(f"{time_elapsed:.2f}\t\t{current_voltage:.2f}\t\t{control_signal:.2f}")

        # Wait for the next time step
        time.sleep(time_step)
        time_elapsed += time_step

    print("Target voltage reached!")
    
    




# Parameters
initial_voltage = influx_data[0]# Starting voltage (can be 200V or 250V)
print(f"initial voltage: {initial_voltage}")
target_voltage = (230 + initial_voltage)/2    # Desired voltage
print(f"target voltage: {target_voltage}")
Kp = 2              # Proportional gain (tune as needed)
Ki = 0.1              # Integral gain (tune as needed)
Kd = 0.05             # Derivative gain (tune as needed)

# Run simulation
simulate_inverter(initial_voltage, target_voltage, Kp, Ki, Kd)