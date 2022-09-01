from typing import TypedDict
class FikaSensorState(TypedDict):
        piston_position: float
        water_temp: float
        has_water: bool
        water_flow: float
        water_pressure: float
        weight: float
        piston_speed: float
        motor_encoder: float