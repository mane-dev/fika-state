import pytest
from ..fika_profile_engine._engine import Fika 
from tests.mock_driver import FikaMockDriver

initial_state={"has_water": True, "piston_position": 0, "water_temp": 0, "water_flow": 0, "water_pressure": 0, "weight": 0, "piston_speed": 0, "motor_encoder": 0}
driver = FikaMockDriver(initial_state)
profile = Fika(profile_path="/home/joheredi/prototypes/statemachine/initialize.json", driver=driver)

profile.run()