# Fika Profile Engine library for Python

This is a library for the Fika Profile Engine. It is a Python library that implements a state machine to execute any Fika Profile.

## Features

* Fika - Is the profile engine
* Driver - Interface to implement which is used by the engine to execute the profile

## Usage

### Create a new virtual environment

```bash
$ python3.10 -m venv venv  
$ source venv/bin/activate
```

### Install the library

> pip install -i https://test.pypi.org/simple/ fika-profile-engine    

### Add a file .vscode/settings.json with the following content:

```json
{
    "python.analysis.extraPaths": [
        "./venv/lib64/python3.10/site-packages"
    ]
}
```

### Implementing a mock driver

```python
import time
from fika_profile_engine import Driver
from fika_profile_engine import FikaSensorState

class FikaMockDriver(Driver):
    def __init__(self, initialState:FikaSensorState):
        self.state = initialState

    def get_sensor_data(self) -> FikaSensorState:
        return self.state

    def update_state(self, state: FikaSensorState):
        updated = {**self.state, **state}
        self.state = updated

    def set_water_temp(self, params):
        current_sensor_state = self.state
        water_temp = current_sensor_state["water_temp"]
        target_temp = params["y"]
        print(f'Current temp: {water_temp}')

        if water_temp >= target_temp:
            print(f'Water is already at target temp {water_temp}')
        else:
            print(f'Heating water to {target_temp}')
            time.sleep(2)
            self.update_state({"water_temp": target_temp})

        return self.state

    def set_water_flow(self, params):
        current_sensor_state = self.state
        water_flow = current_sensor_state["water_flow"]
        target_flow = params["value"]
        print(f'Current flow: {water_flow}')

        if water_flow >= target_flow:
            print(f'Water is already at target flow {water_flow}')
        else:
            print(f'Increasing water flow to {target_flow}')
            time.sleep(2)
            self.update_state({"water_flow": target_flow})

        return self.state

    def set_water_pressure(self, params):
        current_sensor_state = self.state
        water_pressure = current_sensor_state["water_pressure"]
        target_pressure = params["value"]
        print(f'Current pressure: {water_pressure}')

        if water_pressure >= target_pressure:
            print(f'Water is already at target pressure {water_pressure}')
        else:
            print(f'Increasing water pressure to {target_pressure}')
            time.sleep(2)
            self.update_state({"water_pressure": target_pressure})

        return self.state

    def set_weight(self, params):
        current_sensor_state = self.state
        weight = current_sensor_state["weight"]
        target_weight = params["value"]
        print(f'Current weight: {weight}')

        if weight >= target_weight:
            print(f'Already at target weight {weight}')
        else:
            print(f'Increasing weight to {target_weight}')
            time.sleep(2)
            self.update_state({"weight": target_weight})

        return self.state

    def tare(self, params):
        print(f'Executing Tare')
        return self.state

    def position_reference(self, params):
        print(f'Executing Position Reference')
        return self.state

    def log(self, params):
        message = params["value"]
        print(f'Logging: {message}')
        return self.state

    def move_piston(self, params):
        current_sensor_state = self.state
        piston_position = current_sensor_state["piston_position"]
        print(f'Current Piston Position: {piston_position}')
        speed = params["speed"]
        targetPosition = params["value"]
        if piston_position < targetPosition:
            print(f'Moving piston forward at {speed}mm/s')
            time.sleep(2)
            self.update_state({"piston_position": targetPosition})
        elif piston_position > targetPosition:
            print(f'Moving piston backward at {speed}mm/s')
            waitFor = (piston_position - targetPosition)/speed
            time.sleep(waitFor)
            self.update_state({"piston_position": targetPosition})
        else:
            print(f'Piston is already at target')

        return self.state

```

## using the library

```python
import json
from fika_profile_engine import Fika 
from mock_driver import FikaMockDriver

# Open the JSON definition of the profile to run
f = open ('initialize.json', "r")
profile_definition = json.load(f)

# Create a new instance of the Driver implementation
driver = FikaMockDriver()
# Create a new instance of the Fika profile engine with the driver and profile definition
profile = Fika(profile=profile_definition, driver=driver)

# Create an iterator to run the profile
profile_iterator = iter(profile)

# Run the profile, this will loop until the end node is reached
for node in profile_iterator:
    # Print the current node
    print(node["id"])

# Alternatively we can run step by step
# profile.__next__()
```