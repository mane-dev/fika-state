import json
from typing import Any, Callable, List
from reactivex import operators, Subject, throw
from time import time
from action import Action, MovePistonAction

from transition import PistonPositionTransition, TimeoutTransition, Transition, WakeTransition, WaterCheckTransition, WaterTempTransition
from action import Action, MovePistonAction, ErrorAction, SleepAction, TimeoutAction, WaterTempPID1Action

class Finished(Exception):
    pass

class Fika:
    def __init__(self, json_path):
        with open(json_path) as jsonfile:
            flow = json.load(jsonfile)

        self.states = {}

        for stage in flow["stages"]:
            for state in stage['states']:
                self.states[state["id"]] = state

        start = self.states.get("start", None)

        if start == None:
            raise Exception("No start state defined")

        self.current_state = start
        self.stopped = False

        self.status = Subject()
        self.foo_event = Subject()
        self.status.subscribe(lambda x: self.handle_status_update(x))

    def handle_status_update(self, payload):
        if payload.get("kind", None) != 'status_update':
            return
        
        print(self.current_state["id"])
        if self.current_state["id"] == "end":
            raise Finished("Finished")
        target = self.evaluate_transitions(payload=payload.get("payload", None))

        if target != None:
            self.current_state = self.states[target]
        else:
            self.execute_controller()

        

    def execute_controller(self):
        actionSwitch: dict[str, Callable[[Any], Action]] = {
            "move_piston": lambda params: MovePistonAction(params, self.action_event),
            "error": lambda params: ErrorAction(params, self.action_event),
            "sleep": lambda params: SleepAction(params, self.action_event),
            "timeout": lambda params: TimeoutAction(params, self.action_event),
            "water_temp_pid_1": lambda params: WaterTempPID1Action(params, self.action_event)
        }

        for item in self.current_state["actions"]:
            ActionClass = actionSwitch.get(item["kind"], None)

            if ActionClass == None:
                continue

            action = ActionClass(item["parameters"])

            action.start()

    def evaluate_transitions(self, payload):
        transitionSwitch: dict[str, Callable[[Any], Transition]] = {
            "piston_position": lambda operator, value, tag=None: PistonPositionTransition(operator, value, tag),
            "water_check": lambda operator, value, tag=None: WaterCheckTransition(operator, value, tag),
            "water_temp": lambda operator, value, tag=None: WaterTempTransition(operator, value, tag),
            "timeout": lambda operator, value, tag=None: TimeoutTransition(operator, value, tag),
            "wake": lambda operator, value, tag=None: WakeTransition(operator, value, tag)
        }

        
        for item in self.current_state["transitions"]:
            TransitionClass = transitionSwitch.get(item["kind"], None)

            if TransitionClass == None:
                continue

            transition: Transition = TransitionClass(
                operator=item["operator"], value=item.get("value"), tag=item.get("tag", None))

            if transition.evaluate(payload=payload) == True:
                return item["target"]

    def status_update(self, payload):
        self.status.as_observer().on_next(
            {"kind": "status_update", "payload": payload})

    def action_event(self, payload):
        self.foo_event.as_observer().on_next(
            {"kind": "action_event", "payload": payload})


# f = Fika('/home/joheredi/prototypes/statemachine/test.json')

# f.status_update({"piston_position": {"value": 50}})
# f.status_update({"piston_position": {"value": 60}})
# f.status_update({"water_check": {"value": False}})
# f.status_update({"wake": {"value": True}})
# f.status_update({"water_check": {"value": False}})
# f.status_update({"wake": {"value": True}})
# f.status_update({"water_check": {"value": False}})
# f.status_update({"wake": {"value": True}})
# f.status_update({"water_check": {"value": True}})
# f.status_update({"water_temp": {"value": 25}})
# f.status_update({"water_temp": {"value": 30}})
# f.status_update({"water_temp": {"value": 35}})
# f.status_update({"water_temp": {"value": 50}})
# f.status_update({"water_temp": {"value": 65}})
# f.status_update({"water_temp": {"value": 75}})
# f.status_update({"water_temp": {"value": 80}})
# f.status_update({"water_temp": {"value": 82}})
# f.status_update({"water_temp": {"value": 84}})
# f.status_update({"water_temp": {"value": 85}})
# f.status_update({"water_temp": {"value": 86}})
# f.status_update({"water_temp": {"value": 87}})
# f.status_update({"water_temp": {"value": 88}})
# f.status_update({"water_temp": {"value": 89}})
# f.status_update({"water_temp": {"value": 90}})
# f.status_update({"wake": {"value": True}})
# f.status_update({"piston_position": {"value": 59}})
# f.status_update({"piston_position": {"value": 58}})
# f.status_update({"piston_position": {"value": 57}})
# f.status_update({"piston_position": {"value": 56}})
# f.status_update({"piston_position": {"value": 54}})
# f.status_update({"wake": {"value": True}})
# f.status_update({"piston_position": {"value": 40}})
# f.status_update({"piston_position": {"value": 30}})
# f.status_update({"piston_position": {"value": 20}})
# f.status_update({"piston_position": {"value": 10}})
# f.status_update({"piston_position": {"value": 5}})
# f.status_update({"piston_position": {"value": 3}})
# f.status_update({"piston_position": {"value": 2}})
# f.status_update({"piston_position": {"value": 1}})
# f.status_update({"piston_position": {"value": 0}})
# f.status_update({"wake": {"value": True}})