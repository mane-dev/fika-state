import time
from fika_observable import Fika, Finished

class FikaDemo:
    piston_position = 0
    water_temp = 25
    water_check = True
    timeouts = {}

    def __init__(self):
        self.flow = Fika(
            '/home/joheredi/prototypes/statemachine/test.json')
        self.flow.foo_event.subscribe(
            lambda payload: self.handle_execute_action(payload))

    def send_status(self):
        self.flow.status_update(
            {
                "piston_position": {"value": self.piston_position},
                "water_temp": {"value": self.water_temp},
                "water_check": {"value": self.water_check}
            })

    def handle_execute_action(self, payload):
        event_type = payload.get("kind", None)
        if event_type != "action_event":
            return
        payload = payload.get("payload", None)
        self.execute_controller(payload)

    def execute_controller(self, payload):
        actionSwitch = {
            "move_piston": self.MovePiston,
            "error": lambda params: self.ReportError(params),
            "sleep": lambda params: self.Sleep(params),
            "timeout": lambda params: self.Timeout(params),
            "water_temp_pid_1": lambda params: self.WaterTempPID1(params)
        }

        for actionKey in payload:
            action = actionSwitch.get(actionKey, None)
            if action == None:
                continue
            action(payload[actionKey])

    def MovePiston(self, params):
        print(f'Current Piston Position: {self.piston_position}')
        speed = params["speed"]
        targetPosition = params["value"]
        if self.piston_position < targetPosition:
            print(f'Moving piston forward at {speed}mm/s')
            waitFor = (targetPosition - self.piston_position)/speed
            time.sleep(2)
            self.piston_position = targetPosition
        elif self.piston_position > targetPosition:
            print(f'Moving piston backward at {speed}mm/s')
            waitFor = (self.piston_position - targetPosition)/speed
            time.sleep(waitFor)
            self.piston_position = targetPosition
        else:
            print(f'Piston is already at target')

        self.send_status()

    def ReportError(self, params):
        print(f'Error: {params["value"]}')

    def Sleep(self, params):
        print(f'sleeping {params["timeInMs"]}')
        time.sleep(params["timeInMs"])
        self.flow.status_update({"wake": {"value": True}})

    def Timeout(self, params):
        tag = params["tag"]
        timeout = self.timeouts.get(tag, None)

        if timeout == None:
            #setup a new timeout
            timeout = time.time()
            self.timeouts[tag] = timeout

        if time.time() - timeout >= params["value"]:
            self.flow.status_update({"timeout": {"value": True}})
        else:
            self.flow.status_update({"timeout": {"value": False}})

    def WaterTempPID1(self, params):
        print(f'Current Piston Position: {self.piston_position}')
        targetTemp = params["y"]
        mode = params["mode"]
        if self.water_temp < targetTemp:
            print(f'Heating water with {mode}')
            time.sleep(2)
            self.water_temp = targetTemp
            self.send_status()
        else:
            print(f'Water is at temp')


demo = FikaDemo()

while True:
    try:
        demo.send_status()
    except Finished:
        break