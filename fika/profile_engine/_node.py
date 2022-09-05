from typing import Any, Iterable, Literal, TypedDict

class Trigger(TypedDict):
    kind: Literal["water_temperature", "water_flow", "water_pressure", "weight", "timer", "piston_position", "piston_speed", "motor_encoder", "has_water"]
    operator: str
    value: Any
    target: str

class Controller(TypedDict):
    kind: Literal["set_water_temperature", "set_water_flow", "set_water_pressure","set_weight", "move_piston", "tare", "position_reference", "timer", "log"]
    parameters: dict

class Node(TypedDict):
    id: str
    triggers: Iterable[Trigger]
    controllers: Iterable[Controller]

class Stage(TypedDict):
    id: str
    nodes: Iterable[Node]

class Profile(TypedDict):
    stages: Iterable[Stage]